"""Reproduce las dos verificaciones de IA documentadas para Persona 1.

Desde la raíz del repositorio, con el entorno instalado:
MPLBACKEND=Agg .venv/bin/python docs/evidencias_ia/verificar_rosenbrock.py
"""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np
import optimization.gradient_descent_rosenbrock as gd
from optimization.rosenbrock import rosenbrock
from visualization.animations import rosenbrock_isosurface


def main():
    surface_checks = []
    for level in (1, 10):
        branches = rosenbrock_isosurface(np.array(1.0), np.array(1.0), level)
        points = [[1.0, 1.0, float(z)] for z in branches]
        values = [float(rosenbrock(point)) for point in points]
        np.testing.assert_allclose(values, level, rtol=1e-12, atol=1e-12)
        surface_checks.append({"level": level, "points": points, "values": values})

    counts = []
    for initial in ([-1.2, 1.0], [-1.2, 1.0, 0.5]):
        with (
            patch.object(gd, "rosenbrock", wraps=gd.rosenbrock) as objective,
            patch.object(gd, "rosenbrock_gradient", wraps=gd.rosenbrock_gradient) as gradient,
        ):
            result = gd.run_gradient_descent_rosenbrock(initial, iterations=10)
        assert result["function_evaluations"] == objective.call_count == 1
        assert result["gradient_evaluations"] == gradient.call_count == 10
        assert result["status"] == "completed"
        counts.append({
            "dimension": len(initial),
            "initial_point": initial,
            "iterations": 10,
            "actual_function_calls": objective.call_count,
            "actual_gradient_calls": gradient.call_count,
            "equivalent_cost": objective.call_count + 2 * len(initial) * gradient.call_count,
        })

    files = [
        "src/optimization/rosenbrock.py",
        "src/optimization/gradient_descent_rosenbrock.py",
        "visualization/animations.py",
        "docs/evidencias_ia/verificar_rosenbrock.py",
    ]
    evidence = {
        "checked_at": datetime.now(ZoneInfo("America/Bogota")).isoformat(timespec="seconds"),
        "classification": "Verificaciones; no se conserva una respuesta incorrecta literal de IA.",
        "V01_rosenbrock_3d": {
            "f_2d_at_minus1_2_1": float(rosenbrock([-1.2, 1.0])),
            "f_3d_at_minus1_2_1_0_5": float(rosenbrock([-1.2, 1.0, 0.5])),
            "level_sets": surface_checks,
        },
        "V02_evaluation_counts": counts,
        "file_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in files},
    }
    output = Path(__file__).with_name("rosenbrock_verificaciones.json")
    output.write_text(json.dumps(evidence, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
