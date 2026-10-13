
import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import requests

# 1. Rutas de los archivos
DATA_DIR = Path("data/tsp")
CSV_PATH = DATA_DIR / "spain_capitals.csv"
OUTPUT_PATH = DATA_DIR / "matrices_ors.npz"
METADATA_PATH = DATA_DIR / "matrices_ors_metadata.json"

# 2. Configuración de openrouteservice
API_URL = "https://api.openrouteservice.org/v2/matrix/driving-car"
API_KEY = os.environ.get("ORS_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "Falta ORS_API_KEY. Configura la clave en PowerShell."
    )

# 3. Leer las capitales
with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
    ciudades = list(csv.DictReader(f))

if len(ciudades) != 47:
    raise ValueError(
        f"Se esperaban 47 ciudades, pero hay {len(ciudades)}."
    )

nombres = [c["city"] for c in ciudades]

# ORS requiere longitud primero, latitud después
coordenadas = [
    [float(c["lon"]), float(c["lat"])]
    for c in ciudades
]

print(f"Ciudades cargadas: {len(ciudades)}")
print(f"Combinaciones: {len(ciudades) ** 2}")

# 4. Preparar la solicitud
payload = {
    "locations": coordenadas,
    "metrics": ["distance", "duration"],
    "units": "km"
}

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

print("Consultando openrouteservice...")

try:
    respuesta = requests.post(
        API_URL,
        json=payload,
        headers=headers,
        timeout=180
    )
    respuesta.raise_for_status()
    resultado = respuesta.json()

except requests.RequestException as error:
    print("Error al consultar openrouteservice.")
    if "respuesta" in locals():
        print("Estado HTTP:", respuesta.status_code)
        print("Detalle:", respuesta.text[:1500])
    raise SystemExit(1) from error

# 5. Convertir resultados a NumPy
distancias = np.asarray(
    resultado["distances"], dtype=float
)

tiempos = np.asarray(
    resultado["durations"], dtype=float
) / 3600.0

# 6. Validar las matrices
dimension = (47, 47)

for nombre, matriz in [
    ("Distancias", distancias),
    ("Tiempos", tiempos)
]:
    if matriz.shape != dimension:
        raise ValueError(
            f"{nombre}: dimensiones incorrectas {matriz.shape}"
        )

    if not np.all(np.isfinite(matriz)):
        raise ValueError(
            f"{nombre}: contiene valores nulos o infinitos."
        )

    if np.any(matriz < 0):
        raise ValueError(
            f"{nombre}: contiene valores negativos."
        )

    if not np.allclose(np.diag(matriz), 0):
        raise ValueError(
            f"{nombre}: la diagonal no es cero."
        )

print("Validación completada correctamente.")

# 7. Guardar las nuevas matrices
# Los peajes se investigarán por separado.
np.savez_compressed(
    OUTPUT_PATH,
    distances_km=distancias,
    times_hours=tiempos
)

# 8. Guardar información de procedencia
metadata = {
    "fuente": "openrouteservice",
    "endpoint": API_URL,
    "perfil": "driving-car",
    "fecha_consulta_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "ciudades": nombres,
    "numero_ciudades": len(nombres),
    "unidades_distancia": "km",
    "unidades_tiempo": "horas",
    "peajes_incluidos": False,
    "nota": (
        "Estimaciones de rutas por carretera. "
        "No incluyen precios de peajes."
    ),
    "ors_metadata": resultado.get("metadata", {})
}

with METADATA_PATH.open("w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

# 9. Mostrar un resumen
print("\nMatrices generadas correctamente.")
print("Dimensiones:", distancias.shape)
print("Distancia máxima (km):", round(distancias.max(), 2))
print("Tiempo máximo (h):", round(tiempos.max(), 2))
print("Archivo:", OUTPUT_PATH)
print("Metadatos:", METADATA_PATH)
