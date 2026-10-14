"""Archiva el costo total TSP y sus componentes con parámetros y hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tsp.cost_model import compute_total_cost_matrix, load_tsp_data


def export_costs(data_dir, hourly_rate=25.0, toll_multiplier=1.0):
    data_dir = Path(data_dir)
    if not np.isfinite(hourly_rate) or hourly_rate < 0:
        raise ValueError("La tarifa debe ser finita y no negativa.")
    data = load_tsp_data(data_dir)
    consumption = float(data["specs"]["vehicle"]["homologated_consumption_wltp_l_per_100km"])
    price = float(data["specs"]["fuel_price"]["price_eur_per_liter"])
    total = compute_total_cost_matrix(hourly_rate=hourly_rate, toll_multiplier=toll_multiplier, data_dir=data_dir)
    parts = {"time_cost_eur": hourly_rate * data["times_hours"],
             "fuel_cost_eur": consumption / 100 * price * data["distances_km"],
             "toll_cost_eur": toll_multiplier * data["tolls_eur"]}
    for component in parts.values():
        np.fill_diagonal(component, 0.0)
    np.testing.assert_allclose(total, sum(parts.values()), rtol=1e-13, atol=1e-12)
    output = data_dir / "total_cost_matrix.npz"
    np.savez_compressed(output, total_cost_eur=total, **parts)
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    metadata = {
        "schema_version": 1, "units": "EUR", "shape": list(total.shape),
        "hourly_rate_eur_per_h": hourly_rate, "toll_multiplier": toll_multiplier,
        "consumption_l_per_100km": consumption, "fuel_price_eur_per_l": price,
        "formula": "C_ij = w*t_ij + s*p_ij + (c/100)*d_ij*fuel_price; C_ii = 0",
        "directed": True,
        "city_order": [{"matrix_index": i, "id": c["id"], "city": c["city"]}
                       for i, c in enumerate(data["capitals"])],
        "input_sha256": {name: sha(data_dir / name) for name in
                         ("matrices.npz", "vehicle_specs.yaml", "spain_capitals.csv")},
        "output_file": output.name, "output_sha256": sha(output),
        "reproduce": f"python -m scripts.export_tsp_costs --hourly-rate {hourly_rate:g} --toll-multiplier {toll_multiplier:g}",
        "scope": "Matriz de referencia bajo los parámetros indicados; peajes provisionales, no tarifas reales certificadas.",
    }
    (data_dir / "total_cost_matrix_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hourly-rate", type=float, default=25.0)
    parser.add_argument("--toll-multiplier", type=float, default=1.0)
    args = parser.parse_args()
    meta = export_costs(ROOT / "data/tsp", args.hourly_rate, args.toll_multiplier)
    print(f"Matriz total archivada: {meta['shape']}, {meta['hourly_rate_eur_per_h']:g} EUR/h; SHA256 {meta['output_sha256']}")


if __name__ == "__main__":
    main()
