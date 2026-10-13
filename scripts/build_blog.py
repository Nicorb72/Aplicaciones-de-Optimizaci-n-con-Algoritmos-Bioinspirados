
from pathlib import Path
import json
import shutil

# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

# Resultados Parte 1
PARTE1 = (
    ROOT
    / "results"
    / "part1"
    / "comparisons"
    / "all"
    / "comparison.json"
)

# Resultados Parte 2
TSP = ROOT / "results" / "tsp"

# Carpeta principal del blog
DOCS = ROOT / "docs"

# Archivo JSON utilizado por las tablas del blog
SALIDA = DOCS / "datos" / "resultados_blog.json"


# ============================================================
# CARGAR ARCHIVOS JSON
# ============================================================

def cargar_json(ruta):
    if not ruta.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


# ============================================================
# SINCRONIZAR GRÁFICAS Y ANIMACIONES
# ============================================================

def sincronizar_imagenes():

    origen = ROOT / "results"
    destino = DOCS / "imagenes"

    extensiones = {
        ".png",
        ".gif",
        ".jpg",
        ".jpeg",
        ".svg",
    }

    total = 0

    if not origen.exists():
        print("No se encontró la carpeta results.")
        return

    for archivo in origen.rglob("*"):

        if not archivo.is_file():
            continue

        if archivo.suffix.lower() not in extensiones:
            continue

        # Mantener la estructura original de carpetas
        ruta_relativa = archivo.relative_to(origen)

        ruta_destino = destino / ruta_relativa

        ruta_destino.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Copiar o actualizar la imagen
        shutil.copy2(
            archivo,
            ruta_destino,
        )

        total += 1

    print(
        f"Imágenes y animaciones sincronizadas: {total}"
    )


# ============================================================
# GENERAR DATOS DE LA PARTE 1
# ============================================================

def generar_parte1():

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

            "evaluaciones_funcion":
                resumen["mean_function_evaluations"],

            "evaluaciones_gradiente":
                resumen["mean_gradient_evaluations"],

            "costo_equivalente":
                resumen["mean_equivalent_evaluations"],

        })

    print(
        f"Configuraciones Parte 1: {len(parte1)}"
    )

    return parte1


# ============================================================
# GENERAR DATOS DE LA PARTE 2
# ============================================================

def generar_parte2():

    parte2 = []

    for algoritmo in ("aco", "ga"):

        ruta = (
            TSP
            / algoritmo
            / "tsp_summary.json"
        )

        datos = cargar_json(ruta)

        desglose = datos["breakdown"]

        parte2.append({

            "metodo": datos["method"],

            "valor_hora": datos["hourly_rate"],

            "costo_total": datos["best_cost_eur"],

            "distancia_km":
                desglose["total_distance_km"],

            "tiempo_horas":
                desglose["total_time_hours"],

            "combustible_eur":
                desglose["fuel_cost_eur"],

            "peajes_eur":
                desglose["toll_cost_eur"],

            "tiempo_eur":
                desglose["time_cost_eur"],

            "ruta": datos["tour_cities"],

        })

    print(
        f"Algoritmos Parte 2: {len(parte2)}"
    )

    return parte2


# ============================================================
# GENERADOR PRINCIPAL DEL BLOG
# ============================================================

def main():

    print("=== GENERADOR DEL BLOG ===")

    # Obtener resultados de los experimentos
    parte1 = generar_parte1()

    parte2 = generar_parte2()

    # Unificar información del blog
    resultado = {

        "parte1": parte1,

        "parte2": parte2,

    }

    # Crear carpeta de datos si no existe
    SALIDA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Generar archivo JSON actualizado
    with SALIDA.open(
        "w",
        encoding="utf-8",
    ) as archivo:

        json.dump(
            resultado,
            archivo,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )

    print(
        f"Archivo JSON actualizado: {SALIDA}"
    )

    # Sincronizar todas las gráficas y animaciones
    sincronizar_imagenes()

    print(
        "\nBlog actualizado correctamente."
    )


if __name__ == "__main__":
    main()
