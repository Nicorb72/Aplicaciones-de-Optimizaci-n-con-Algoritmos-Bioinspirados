"""Comprueba el comando completo con corridas cortas y salidas temporales."""

import csv
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image
import yaml


def test_persona1_command_generates_both_dimensions_and_gifs(tmp_path):
    root = Path(__file__).resolve().parents[1]
    config_paths = []
    for dimension in (2, 3):
        config = {
            "function": "rosenbrock", "dimension": dimension,
            "domain": {"lower": -1, "upper": 1}, "learning_rate": 0.0001,
            "iterations": 3, "runs": 30, "success_threshold": 0.0001,
            "seed": 42, "output_dir": str(tmp_path / "raw"),
        }
        path = tmp_path / f"config_{dimension}d.yaml"
        path.write_text(yaml.safe_dump(config), encoding="utf-8")
        config_paths.append(path)
    env = dict(os.environ, PYTHONPATH=str(root / "src"), MPLBACKEND="Agg")
    env.setdefault("MPLCONFIGDIR", str(tmp_path / "mplconfig"))
    result = subprocess.run(
        [sys.executable, "-m", "experiments.run_persona1",
         "--config-2d", str(config_paths[0]), "--config-3d", str(config_paths[1]),
         "--figures-dir", str(tmp_path / "figures"),
         "--animations-dir", str(tmp_path / "animations"),
         "--frames", "2", "--fps", "5", "--run-id", "run_002"],
        cwd=root, env=env, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for dimension in (2, 3):
        raw = tmp_path / "raw" / f"{dimension}d"
        payload = json.loads((raw / "summary.json").read_text(encoding="utf-8"))
        assert payload["config"]["dimension"] == dimension
        assert payload["summary"]["runs"] == 30
        with (raw / "runs.csv").open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        assert [int(row["seed"]) for row in rows] == list(range(42, 72))
        assert all(int(row["gradient_evaluations"]) == 3 for row in rows)
        with np.load(raw / "trajectories.npz", allow_pickle=False) as data:
            assert len(data.files) == 30
            assert data["run_002"].shape == (4, dimension)
        for name in ("convergence.png", "trajectory_run_001.png"):
            with Image.open(tmp_path / "figures" / f"{dimension}d" / name) as picture:
                assert picture.format == "PNG"
                picture.verify()
        with Image.open(tmp_path / "animations" / f"{dimension}d/trajectory_run_002.gif") as gif:
            assert gif.format == "GIF"
            assert gif.n_frames == 2
            assert gif.info["duration"] == 200
