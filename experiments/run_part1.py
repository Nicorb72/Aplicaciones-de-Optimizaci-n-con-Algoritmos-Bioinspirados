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

            if algorithm == "gd":
                dims = suite["gd_dimensions"]
            else:
                dims = suite["heuristic_dimensions"]

            for dim in ([dimension] if dimension is not None else dims):

                params = dict(parameters)

                if algorithm == "gd":
                    params["learning_rate"] = problem["learning_rate"]

                yield {
                    "function": name,
                    "method": algorithm,
                    "dimension": dim,
                    "domain": problem["domain"],
                    "parameters": params,
                    "runs": suite["runs"],
                    "seed": suite["seed"],
                    "success_threshold": suite["success_threshold"],
                }


def apply_evolutionary_overrides(suite, args):
    """Reemplaza parámetros del evolutivo cuando se indican por terminal."""

    evolutionary = suite["methods"]["evolutionary"]

    overrides = {
        "population_size": args.population_size,
        "generations": args.generations,
        "tournament_size": args.tournament_size,
        "crossover_alpha": args.crossover_alpha,
        "mutation_rate": args.mutation_rate,
        "mutation_sigma": args.mutation_sigma,
        "elite_fraction": args.elite_fraction,
    }

    for parameter, value in overrides.items():
        if value is not None:
            evolutionary[parameter] = value


def print_evolutionary_config(config):
    """Muestra la configuración efectiva del algoritmo evolutivo."""

    parameters = config["parameters"]

    population_size = parameters["population_size"]
    elite_fraction = parameters["elite_fraction"]

    elite_size = max(
        1,
        round(population_size * elite_fraction),
    )

    evaluations = (
        population_size
        + (population_size - elite_size)
        * parameters["generations"]
    )

    print(
        "  Evolutivo: "
        f"población={population_size}, "
        f"generaciones={parameters['generations']}, "
        f"torneo={parameters['tournament_size']}, "
        f"alpha={parameters['crossover_alpha']}, "
        f"mutación={parameters['mutation_rate']}, "
        f"sigma={parameters['mutation_sigma']}, "
        f"élite={elite_size} de {population_size}, "
        f"evaluaciones={evaluations}",
        flush=True,
    )


def main(default_method=None):
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs/part1.yaml",
    )

    parser.add_argument(
        "--method",
        choices=["gd", "pso", "evolutionary", "de"],
        default=default_method,
    )

    parser.add_argument(
        "--function",
        choices=["rosenbrock", "rastrigin"],
    )

    parser.add_argument(
        "--dimension",
        type=int,
        choices=[2, 3],
    )

    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--frames", type=int)
    parser.add_argument("--fps", type=int)

    parser.add_argument(
        "--pacing",
        choices=["iterations", "movement"],
        help="Ritmo por iteraciones o por movimiento con interpolación visual.",
    )

    # Parámetros modificables del algoritmo evolutivo
    parser.add_argument(
        "--population-size",
        type=int,
        help="Tamaño de la población del algoritmo evolutivo.",
    )

    parser.add_argument(
        "--generations",
        type=int,
        help="Número de generaciones del algoritmo evolutivo.",
    )

    parser.add_argument(
        "--tournament-size",
        type=int,
        help="Número de individuos que participan en cada torneo.",
    )

    parser.add_argument(
        "--crossover-alpha",
        type=float,
        help="Valor alpha utilizado en el cruce BLX-alpha.",
    )

    parser.add_argument(
        "--mutation-rate",
        type=float,
        help="Probabilidad de mutación de cada variable.",
    )

    parser.add_argument(
        "--mutation-sigma",
        type=float,
        help="Desviación estándar de la mutación gaussiana.",
    )

    parser.add_argument(
        "--elite-fraction",
        type=float,
        help="Fracción de la población conservada mediante elitismo.",
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--no-visuals",
        action="store_true",
        help="Ejecuta y guarda experimentos y tabla, sin renderizar.",
    )

    mode.add_argument(
        "--render-only",
        action="store_true",
        help=(
            "Regenera gráficos/GIF/tabla desde resultados existentes "
            "de la misma configuración."
        ),
    )

    args = parser.parse_args()

    suite = yaml.safe_load(
        args.config.read_text(encoding="utf-8")
    )

    # Los valores indicados por terminal reemplazan temporalmente
    # la configuración del YAML únicamente para el evolutivo.
    apply_evolutionary_overrides(suite, args)

    output = args.output_dir or Path(suite["output_dir"])

    if not output.is_absolute():
        output = ROOT / output

    frames = (
        args.frames
        if args.frames is not None
        else suite["animation"]["frames"]
    )

    fps = (
        args.fps
        if args.fps is not None
        else suite["animation"]["fps"]
    )

    if frames < 2 or not 1 <= fps <= 100:
        parser.error(
            "Se requiere frames >= 2 y fps entre 1 y 100."
        )

    pacing = (
        args.pacing
        or suite["animation"].get("pacing", "iterations")
    )

    rows = []

    for config in configurations(
        suite,
        args.method,
        args.function,
        args.dimension,
    ):
        relative = (
            Path(config["function"])
            / config["method"]
            / f"{config['dimension']}d"
        )

        raw = output / "raw" / relative

        print(
            f"Procesando {relative} · "
            f"{config['runs']} corridas",
            flush=True,
        )

        # Se muestra una sola vez la configuración efectiva.
        if config["method"] == "evolutionary":
            print_evolutionary_config(config)

        if args.render_only:

            saved = json.loads(
                (raw / "summary.json").read_text(
                    encoding="utf-8"
                )
            )

            if saved["config"] != config:
                raise ValueError(
                    f"La configuración guardada en {raw} "
                    "no coincide; ejecuta primero los experimentos."
                )

            summary = saved["summary"]

        else:

            results, summary = run_configuration(config)

            save_results(
                results,
                summary,
                config,
                raw,
            )

        rows.append(
            {
                "config": config,
                "summary": summary,
            }
        )

        print(
            f"  Éxitos "
            f"{summary['successful_runs']}/"
            f"{summary['runs']}; "
            f"costo equivalente medio "
            f"{summary['mean_equivalent_evaluations']:.1f}",
            flush=True,
        )

        if not args.no_visuals:

            plot_configuration(
                raw,
                output / "figures" / relative,
            )

            run_id = select_run(raw)

            if (
                run_id
                and config["method"] in ("gd", "pso")
            ):
                path = animate_saved(
                    raw,
                    output / "animations" / relative.parent,
                    run_id,
                    frames,
                    fps,
                    pacing,
                )

                print(
                    f"  GIF: {path}",
                    flush=True,
                )

    if not rows:
        parser.error(
            "Los filtros no seleccionaron ninguna configuración."
        )

    # Cada selección conserva su propia comparación;
    # no reemplaza la tabla completa.
    tag = "_".join(
        str(value)
        for value in [
            args.function,
            args.method,
            args.dimension,
        ]
        if value is not None
    )

    report_dir = (
        output
        / "comparisons"
        / (tag or "all")
    )

    write_comparison(
        rows,
        report_dir,
        output,
        include_figures=not args.no_visuals,
    )

    print(
        f"Comparación: {report_dir / 'report.md'}",
        flush=True,
    )

    print(
        f"Informe visual: {report_dir / 'report.html'}",
        flush=True,
    )


if __name__ == "__main__":
    main()