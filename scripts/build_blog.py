
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

PARTE1 = ROOT / "results" / "part1" / "comparisons" / "all" / "comparison.json"
TSP = ROOT / "results" / "tsp"
DOCS = ROOT / "docs"

SALIDA = DOCS / "datos" / "resultados_blog.json"


def cargar_json(ruta):
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró: {ruta}")

    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def main():
    print("=== GENERADOR DE DATOS DEL BLOG ===")

    # Parte 1: optimización numérica
    registros = cargar_json(PARTE1)

    parte1 = []

    for registro in registros:
        config = registro["config"]
        resumen = registro["summary"]

        parte1.append({
            "funcion": config["function"],
            "metodo": config["method"],
            "dimension": config["dimension"],
            "corridas": resumen["runs"],
            "exitos": resumen["successful_runs"],
            "tasa_exito": resumen["success_rate"],
            "media": resumen["mean_value"],
            "desviacion": resumen["std_value"],
            "mejor": resumen["best_value"],
            "peor": resumen["worst_value"],
            "evaluaciones_funcion": resumen["mean_function_evaluations"],
            "evaluaciones_gradiente": resumen["mean_gradient_evaluations"],
            "costo_equivalente": resumen["mean_equivalent_evaluations"],
        })

    # Parte 2: problema del viajero
    parte2 = []

    for algoritmo in ("aco", "ga"):
        ruta = TSP / algoritmo / "tsp_summary.json"
        datos = cargar_json(ruta)
        desglose = datos["breakdown"]

        parte2.append({
            "metodo": datos["method"],
            "valor_hora": datos["hourly_rate"],
            "costo_total": datos["best_cost_eur"],
            "distancia_km": desglose["total_distance_km"],
            "tiempo_horas": desglose["total_time_hours"],
            "combustible_eur": desglose["fuel_cost_eur"],
            "peajes_eur": desglose["toll_cost_eur"],
            "tiempo_eur": desglose["time_cost_eur"],
            "ruta": datos["tour_cities"],
        })

    # Información final del blog
    resultado = {
        "parte1": parte1,
        "parte2": parte2,
    }

    SALIDA.parent.mkdir(parents=True, exist_ok=True)

    with SALIDA.open("w", encoding="utf-8") as archivo:
        json.dump(
            resultado,
            archivo,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )

    print(f"Configuraciones Parte 1: {len(parte1)}")
    print(f"Algoritmos Parte 2: {len(parte2)}")
    print(f"Archivo generado: {SALIDA}")
    print("Datos del blog actualizados correctamente.")


if __name__ == "__main__":
    main()
