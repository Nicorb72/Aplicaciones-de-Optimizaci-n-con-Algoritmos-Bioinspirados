
from pathlib import Path
from datetime import datetime, timezone
import json
import shutil
import numpy as np

carpeta = Path("data/tsp")

original = carpeta / "matrices.npz"
ors = carpeta / "matrices_ors.npz"
respaldo = carpeta / "matrices_original_backup.npz"

# Guardar respaldo de la matriz original
if not respaldo.exists():
    shutil.copy2(original, respaldo)

with np.load(respaldo) as datos:
    peajes = datos["tolls_eur"].copy()

with np.load(ors) as datos:
    distancias = datos["distances_km"].copy()
    tiempos = datos["times_hours"].copy()

# Validaciones
for nombre, matriz in [
    ("Distancias", distancias),
    ("Tiempos", tiempos),
    ("Peajes", peajes),
]:
    assert matriz.shape == (47, 47), nombre
    assert np.isfinite(matriz).all(), nombre
    assert (matriz >= 0).all(), nombre
    np.fill_diagonal(matriz, 0)

# Integrar en el formato que espera el proyecto
np.savez_compressed(
    original,
    distances_km=distancias,
    times_hours=tiempos,
    tolls_eur=peajes
)

# Registrar procedencia y limitaciones
documentacion = {
    "fecha_integracion_utc":
        datetime.now(timezone.utc).isoformat(),
    "distancias": "openrouteservice driving-car",
    "tiempos": "openrouteservice driving-car",
    "peajes": "matriz original del proyecto, provisional",
    "advertencia": (
        "Los peajes no estan verificados para las "
        "2162 rutas dirigidas. Los valores cero "
        "pueden representar ausencia de datos "
        "y no necesariamente ausencia de peaje."
    ),
    "vehiculo": "SEAT Leon 1.5 TSI",
    "estado": "provisional"
}

with (carpeta / "integration_notes.json").open(
    "w", encoding="utf-8"
) as archivo:
    json.dump(
        documentacion,
        archivo,
        ensure_ascii=False,
        indent=2
    )

print("MATRICES INTEGRADAS CORRECTAMENTE")
print("Dimensiones:", distancias.shape)
print("Distancia media:", round(distancias.mean(), 2))
print("Tiempo medio:", round(tiempos.mean(), 2))
print("Peajes positivos:", np.count_nonzero(peajes))
print("Respaldo:", respaldo)
print("Archivo final:", original)
print("ADVERTENCIA: peajes provisionales")
