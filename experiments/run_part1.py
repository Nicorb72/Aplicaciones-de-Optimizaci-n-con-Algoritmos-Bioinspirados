"""Experimentos reproducibles de la Parte 1: dos funciones y cuatro métodos."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

import yaml
from optimization.benchmark import run_configuration
from optimization.result_storage import save_results
from optimization.comparison import write_comparison
from visualization.animations import animate_saved
from visualization.plot_benchmark import plot_configuration, select_run


def configurations(suite, method=None, function=None, dimension=None):
    for name, problem in suite["functions"].items():
        if function is not None and name != function:
            continue
        for algorithm, parameters in suite["methods"].items():
            if method is not None and algorithm != method:
                continue
            dims = suite["gd_dimensions"] if algorithm == "gd" else suite["heuristic_dimensions"]
            for dim in ([dimension] if dimension is not None else dims):
                params = dict(parameters)
                if algorithm == "gd":
                    params["learning_rate"] = problem["learning_rate"]
                yield {"function": name, "method": algorithm, "dimension": dim,
                       "domain": problem["domain"], "parameters": params,
                       "runs": suite["runs"], "seed": suite["seed"],
                       "success_threshold": suite["success_threshold"]}


def main(default_method=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/part1.yaml")
    parser.add_argument("--method", choices=["gd", "pso", "evolutionary", "de"], default=default_method)
    parser.add_argument("--function", choices=["rosenbrock", "rastrigin"])
    parser.add_argument("--dimension", type=int, choices=[2, 3])
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--frames", type=int)
    parser.add_argument("--fps", type=int)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--no-visuals", action="store_true", help="Ejecuta y guarda experimentos y tabla, sin renderizar.")
    mode.add_argument("--render-only", action="store_true", help="Regenera gráficos/GIF/tabla desde resultados existentes de la misma configuración.")
    args = parser.parse_args()
    suite = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    output = args.output_dir or Path(suite["output_dir"])
    if not output.is_absolute():
        output = ROOT / output
    frames = args.frames if args.frames is not None else suite["animation"]["frames"]
    fps = args.fps if args.fps is not None else suite["animation"]["fps"]
    if frames < 2 or not 1 <= fps <= 100:
        parser.error("Se requiere frames >= 2 y fps entre 1 y 100.")
    rows = []
    for config in configurations(suite, args.method, args.function, args.dimension):
        relative = Path(config["function"]) / config["method"] / f"{config['dimension']}d"
        raw = output / "raw" / relative
        print(f"Procesando {relative} · {config['runs']} corridas", flush=True)
        if args.render_only:
            saved = json.loads((raw / "summary.json").read_text(encoding="utf-8"))
            if saved["config"] != config:
                raise ValueError(f"La configuración guardada en {raw} no coincide; ejecuta primero los experimentos.")
            summary = saved["summary"]
        else:
            results, summary = run_configuration(config)
            save_results(results, summary, config, raw)
        rows.append({"config": config, "summary": summary})
        print(f"  Éxitos {summary['successful_runs']}/{summary['runs']}; costo equivalente medio {summary['mean_equivalent_evaluations']:.1f}", flush=True)
        if not args.no_visuals:
            plot_configuration(raw, output / "figures" / relative)
            run_id = select_run(raw)
            if run_id and config["method"] in ("gd", "pso"):
                path = animate_saved(raw, output / "animations" / relative.parent, run_id, frames, fps)
                print(f"  GIF: {path}", flush=True)
    if not rows:
        parser.error("Los filtros no seleccionaron ninguna configuración.")
    # Cada selección conserva su propia comparación; no reemplaza la tabla completa.
    tag = "_".join(str(v) for v in [args.function, args.method, args.dimension] if v is not None)
    report_dir = output / "comparisons" / (tag or "all")
    write_comparison(rows, report_dir, output, include_figures=not args.no_visuals)
    print(f"Comparación: {report_dir / 'report.md'}", flush=True)


if __name__ == "__main__":
    main()
