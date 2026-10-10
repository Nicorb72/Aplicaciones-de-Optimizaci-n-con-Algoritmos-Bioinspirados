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


def run_single_tsp(config, hourly_rate=None):
    if hourly_rate is None:
        hourly_rate = float(config.get("hourly_rate", 25.0))

    cost_matrix = compute_total_cost_matrix(hourly_rate=hourly_rate)
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
    result["breakdown"] = get_tour_breakdown(result["best_tour"], hourly_rate=hourly_rate)
    result["hourly_rate"] = hourly_rate
    return result


def tour_edges(tour):
    """Aristas del ciclo, sin importar la ciudad de partida ni el sentido del recorrido."""
    n = len(tour)
    return {frozenset((int(tour[i]), int(tour[(i + 1) % n]))) for i in range(n)}


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Ejecución de optimización TSP en España peninsular.")
    parser.add_argument("--config", type=Path, default=root / "configs/tsp_aco.yaml", help="Archivo YAML de configuración.")
    parser.add_argument("--hourly-rate", type=float, default=None, help="Sobrescribe el valor de la hora del vendedor (€/h).")
    parser.add_argument("--study-hourly-rates", action="store_true", help="Realiza barrido paramétrico sobre el valor de la hora.")
    parser.add_argument("--rates", type=float, nargs="+", default=[0.0, 10.0, 25.0, 50.0, 75.0, 100.0], help="Valores de la hora (€/h) para el estudio paramétrico.")
    parser.add_argument("--study-seeds", type=int, default=1, help="Semillas por valor de la hora en el estudio (se conserva la mejor ruta).")
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
        rates = args.rates
        base_seed = int(config.get("seed", 42))
        study_results = []
        previous_edges = None
        first_change = None
        for rate in rates:
            # Con varias semillas se conserva la mejor ruta, para no confundir azar con efecto real.
            res = None
            for k in range(args.study_seeds):
                candidate = run_single_tsp(dict(config, seed=base_seed + k), hourly_rate=rate)
                if res is None or candidate["best_cost"] < res["best_cost"]:
                    res = candidate
            bd = res["breakdown"]
            print(f"Valor hora: {rate:5.1f} €/h | Costo total: {bd['total_cost_eur']:8.2f} € | Distancia: {bd['total_distance_km']:7.1f} km | Tiempo: {bd['total_time_hours']:5.1f} h", flush=True)
            edges = tour_edges(res["best_tour"])
            changed = None if previous_edges is None else len(edges - previous_edges)
            if changed is not None:
                print(f"    Ruta frente al valor anterior: {changed} aristas distintas", flush=True)
                if changed and first_change is None:
                    first_change = rate
            previous_edges = edges
            study_results.append({
                "hourly_rate": rate,
                "total_cost_eur": bd["total_cost_eur"],
                "distance_km": bd["total_distance_km"],
                "time_hours": bd["total_time_hours"],
                "tour": [int(x) for x in res["best_tour"]],
                "edges_changed_vs_previous": changed,
            })
        if first_change is None:
            print("La ruta no cambió en el rango estudiado.", flush=True)
        else:
            print(f"La ruta cambió por primera vez al pasar al valor de {first_change:g} €/h.", flush=True)
        if args.study_seeds == 1:
            print("Nota: con una sola semilla un cambio puede deberse al azar; use --study-seeds 5 o más para confirmar.", flush=True)
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
