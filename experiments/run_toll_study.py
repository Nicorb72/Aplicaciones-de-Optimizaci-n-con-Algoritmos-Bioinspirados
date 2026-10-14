"""Tres escenarios de peajes provisionales, con semillas emparejadas y rutas dirigidas."""
import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import yaml

from .run_tsp import run_single_tsp

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = [(0.0, "Sin componente de peajes"),
             (1.0, "Peajes provisionales actuales"),
             (2.0, "Peajes provisionales duplicados")]


def directed_edges(tour):
    return set(zip(tour, tour[1:] + tour[:1]))


def run_study(configs, seeds, hourly_rate=25.0):
    records = []
    for config in configs:
        method = config["method"].lower()
        by_seed = {}
        # La referencia se obtiene primero para comparar cada semilla consigo misma.
        for multiplier in (1.0, 0.0, 2.0):
            for seed in seeds:
                start = time.perf_counter()
                result = run_single_tsp(dict(config, seed=seed), hourly_rate, multiplier)
                tour = [int(x) for x in result["best_tour"]]
                baseline = tour if multiplier == 1 else by_seed[seed]
                if multiplier == 1:
                    by_seed[seed] = tour
                matrix = result["cost_matrix"]
                fixed_cost = sum(matrix[u, v] for u, v in zip(baseline, baseline[1:] + baseline[:1]))
                records.append({
                    "method": method, "seed": seed, "toll_multiplier": multiplier,
                    "best_cost_eur": float(result["best_cost"]),
                    "breakdown": {k: float(v) for k, v in result["breakdown"].items()},
                    "tour": tour,
                    "directed_edges_changed_vs_base": len(directed_edges(tour) - directed_edges(baseline)),
                    "base_tour_cost_in_scenario_eur": float(fixed_cost),
                    "elapsed_seconds": time.perf_counter() - start,
                })
                print(f"{method.upper()} semilla={seed} peajes×{multiplier:g}: {result['best_cost']:.2f} EUR", flush=True)
    summaries = []
    for config in configs:
        method = config["method"].lower()
        for multiplier, label in SCENARIOS:
            rows = [r for r in records if r["method"] == method and r["toll_multiplier"] == multiplier]
            best = min(rows, key=lambda r: r["best_cost_eur"])
            values = [r["best_cost_eur"] for r in rows]
            summaries.append({
                "method": method, "scenario": label, "toll_multiplier": multiplier,
                "runs": len(rows), "mean_cost_eur": float(np.mean(values)),
                "std_cost_eur": float(np.std(values, ddof=1)) if len(rows) > 1 else None,
                "best_cost_eur": best["best_cost_eur"], "best_seed": best["seed"],
                "best_breakdown": best["breakdown"],
                "changed_routes": sum(r["directed_edges_changed_vs_base"] > 0 for r in rows),
                "mean_fixed_base_tour_cost_eur": float(np.mean([r["base_tour_cost_in_scenario_eur"] for r in rows])),
            })
    return {"hourly_rate": hourly_rate, "seeds": list(seeds), "configs": configs,
            "scope": "Escenarios hipotéticos sobre la matriz provisional; los ceros desconocidos siguen siendo cero. El factor 0 no implica carreteras gratuitas. El factor 2 no es una cota superior real. Tres semillas no prueban superioridad ni robustez general.",
            "summaries": summaries, "runs": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
    parser.add_argument("--hourly-rate", type=float, default=25.0)
    parser.add_argument("--output", type=Path, default=ROOT / "results/tsp/toll_sensitivity.json")
    args = parser.parse_args()
    if len(set(args.seeds)) != len(args.seeds):
        parser.error("Las semillas no deben repetirse.")
    if not np.isfinite(args.hourly_rate) or args.hourly_rate < 0:
        parser.error("El valor de la hora debe ser finito y no negativo.")
    paths = [ROOT / f"configs/tsp_{m}.yaml" for m in ("aco", "ga")]
    configs = [yaml.safe_load(p.read_text(encoding="utf-8")) for p in paths]
    study = run_study(configs, args.seeds, args.hourly_rate)
    study["input_sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [*paths, ROOT / "data/tsp/matrices.npz", ROOT / "data/tsp/vehicle_specs.yaml"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(study, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(f"Estudio guardado: {args.output}")


if __name__ == "__main__":
    main()
