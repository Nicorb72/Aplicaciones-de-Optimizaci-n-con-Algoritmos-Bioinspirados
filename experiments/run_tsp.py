import argparse
import json
from pathlib import Path
import sys
import numpy as np
import yaml

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir / "src") not in sys.path:
    sys.path.insert(0, str(root_dir / "src"))

from tsp.cost_model import compute_total_cost_matrix, get_tour_breakdown, load_tsp_data
from tsp.ant_colony import run_ant_colony_tsp
from tsp.genetic_tsp import run_genetic_tsp
from visualization.plot_tsp import plot_spain_tour, animate_tsp_tour_evolution


def run_single_tsp(config, hourly_rate=None, toll_multiplier=1.0):
    if hourly_rate is None:
        hourly_rate = float(config.get("hourly_rate", 25.0))

    cost_matrix = compute_total_cost_matrix(hourly_rate=hourly_rate, toll_multiplier=toll_multiplier)
    method = config.get("method", "aco").lower()

    if method == "aco":
        result = run_ant_colony_tsp(
            cost_matrix=cost_matrix,
            n_ants=config.get("n_ants", 25),
            iterations=config.get("iterations", 80),
            alpha=config.get("alpha", 1.0),
            beta=config.get("beta", 2.5),
            rho=config.get("rho", 0.1),
            q=config.get("q", 100.0),
            seed=config.get("seed", 42),
        )
    elif method == "ga":
        result = run_genetic_tsp(
            cost_matrix=cost_matrix,
            population_size=config.get("population_size", 100),
            generations=config.get("generations", 200),
            mutation_rate=config.get("mutation_rate", 0.25),
            tournament_size=config.get("tournament_size", 4),
            elite_size=config.get("elite_size", 2),
            seed=config.get("seed", 42),
        )
    else:
        raise ValueError(f"Método desconocido: {method}. Debe ser 'aco' o 'ga'.")

    result["cost_matrix"] = cost_matrix
    result["breakdown"] = get_tour_breakdown(result["best_tour"], hourly_rate=hourly_rate,
                                            toll_multiplier=toll_multiplier)
    result["hourly_rate"] = hourly_rate
    return result


def tour_edges(tour):
    """Arcos dirigidos del ciclo; las rotaciones conservan el mismo conjunto."""
    n = len(tour)
    return {(int(tour[i]), int(tour[(i + 1) % n])) for i in range(n)}


def run_hourly_rate_study(config, rates, seeds):
    """Barrido exploratorio con semillas emparejadas y ciclos dirigidos."""
    rates = sorted(set(float(rate) for rate in rates))
    seeds = list(seeds)
    if not rates or not seeds or any(not np.isfinite(r) or r < 0 for r in rates):
        raise ValueError("Se requieren tarifas finitas no negativas y al menos una semilla.")
    previous = {}
    rows = []
    for rate in rates:
        runs = []
        for seed in seeds:
            result = run_single_tsp(dict(config, seed=seed), hourly_rate=rate)
            tour = [int(x) for x in result["best_tour"]]
            edges = tour_edges(tour)
            runs.append({
                "seed": seed, "tour": tour,
                "total_cost_eur": float(result["best_cost"]),
                "breakdown": result["breakdown"],
                "edges_changed_vs_previous": None if seed not in previous else len(edges - previous[seed]),
            })
            previous[seed] = edges
        best = min(runs, key=lambda r: r["total_cost_eur"])
        costs = [r["total_cost_eur"] for r in runs]
        rows.append({
            "hourly_rate": rate,
            "previous_hourly_rate": rows[-1]["hourly_rate"] if rows else None,
            "total_cost_eur": best["total_cost_eur"],
            "distance_km": best["breakdown"]["total_distance_km"],
            "time_hours": best["breakdown"]["total_time_hours"],
            "tour": best["tour"], "best_seed": best["seed"],
            "mean_cost_eur": float(np.mean(costs)),
            "std_cost_eur": float(np.std(costs, ddof=1)) if len(runs) > 1 else None,
            "changed_seeds_vs_previous": None if not rows else sum(r["edges_changed_vs_previous"] > 0 for r in runs),
            "seeds": seeds, "runs": runs, "config": config,
        })
        print(f"{config['method'].upper()} | {rate:g} EUR/h | mejor {best['total_cost_eur']:.2f} EUR | semillas con cambio: {rows[-1]['changed_seeds_vs_previous']}", flush=True)
    return rows


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Ejecución de optimización TSP en España peninsular.")
    parser.add_argument("--config", type=Path, default=root / "configs/tsp_aco.yaml", help="Archivo YAML de configuración.")
    parser.add_argument("--hourly-rate", type=float, default=None, help="Sobrescribe el valor de la hora del vendedor (€/h).")
    parser.add_argument("--study-hourly-rates", action="store_true", help="Realiza barrido paramétrico sobre el valor de la hora.")
    parser.add_argument("--rates", type=float, nargs="+", default=[0.0, 1.0, 2.0, 5.0, 10.0, 25.0, 50.0, 75.0, 100.0], help="Valores de la hora (€/h) para el estudio paramétrico.")
    parser.add_argument("--study-seeds", type=int, default=3, help="Semillas emparejadas por tarifa; se guardan todas las corridas y su mejor ruta.")
    parser.add_argument("--no-gif", action="store_true", help="Omite la generación del GIF de evolución para corridas ultrarrápidas.")
    args = parser.parse_args()

    with args.config.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)

    output_dir = Path(config.get("output_dir", "results/tsp"))
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.study_hourly_rates:
        print("\n=== Estudio paramétrico: Variación del valor de la hora del vendedor ===", flush=True)
        if args.study_seeds < 1:
            parser.error("--study-seeds debe ser al menos 1")
        base_seed = int(config.get("seed", 42))
        study_results = run_hourly_rate_study(config, args.rates, range(base_seed, base_seed + args.study_seeds))
        first = next((r for r in study_results if r["changed_seeds_vs_previous"]), None)
        if first:
            print(f"Primer intervalo con cambio observado: ({first['previous_hourly_rate']:g}, {first['hourly_rate']:g}] EUR/h; {first['changed_seeds_vs_previous']}/{args.study_seeds} semillas. No es un umbral óptimo global.", flush=True)
        else:
            print("Sin cambios observados entre las tarifas muestreadas; no descarta cambios intermedios.", flush=True)
        study_path = output_dir / "hourly_rate_study.json"
        study_path.write_text(json.dumps(study_results, indent=2), encoding="utf-8")
        print(f"Resultados del estudio guardados en: {study_path}", flush=True)
        return

    print(f"\n=== Ejecutando TSP con método {config.get('method', 'aco').upper()} ===", flush=True)
    result = run_single_tsp(config, hourly_rate=args.hourly_rate)
    bd = result["breakdown"]

    data = load_tsp_data()
    city_names = [data["capitals"][i]["city"] for i in result["best_tour"]]

    print(f"Mejor costo total: {result['best_cost']:.2f} €", flush=True)
    print(f"  - Distancia total: {bd['total_distance_km']:.1f} km", flush=True)
    print(f"  - Tiempo de viaje: {bd['total_time_hours']:.1f} h ({bd['time_cost_eur']:.2f} €)", flush=True)
    print(f"  - Combustible: {bd['fuel_cost_eur']:.2f} €", flush=True)
    print(f"  - Peajes: {bd['toll_cost_eur']:.2f} €", flush=True)
    print(f"Secuencia inicial: {' -> '.join(city_names[:6])} ... -> {city_names[0]}", flush=True)

    # Guardar resultados
    tour_plot_path = output_dir / "spain_optimal_tour.png"
    plot_spain_tour(result["best_tour"], result["cost_matrix"], tour_plot_path)
    print(f"Figura guardada en: {tour_plot_path}", flush=True)

    if not args.no_gif and result.get("tour_evolution"):
        gif_path = output_dir / "tour_evolution.gif"
        print("Generando animación del recorrido...", flush=True)
        animate_tsp_tour_evolution(result["tour_evolution"], result["cost_matrix"], gif_path)
        print(f"GIF guardado en: {gif_path}", flush=True)

    summary = {
        "method": result["method"],
        "seed": result["seed"],
        "config": config,
        "hourly_rate": result["hourly_rate"],
        "best_cost_eur": result["best_cost"],
        "breakdown": bd,
        "best_tour": [int(x) for x in result["best_tour"]],
        "tour_cities": city_names,
    }
    summary_path = output_dir / "tsp_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Resumen guardado en: {summary_path}", flush=True)


if __name__ == "__main__":
    main()
