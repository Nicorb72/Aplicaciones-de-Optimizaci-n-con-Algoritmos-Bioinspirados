import csv
import json

import numpy as np
import pytest
import yaml

from experiments.run_rosenbrock_gd import run_experiments
from optimization.result_storage import save_results
from optimization.statistics import summarize_results


@pytest.mark.parametrize("dimension", [2, 3])
def test_saved_results_round_trip(tmp_path, dimension):
    config = {
        "function": "rosenbrock",
        "dimension": dimension,
        "domain": {"lower": -2, "upper": 2},
        "learning_rate": 0.001,
        "iterations": 10,
        "runs": 2,
        "seed": 42,
        "success_threshold": 0.0001,
        "output_dir": "results/raw/rosenbrock_gd",
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    results = run_experiments(config_path)
    summary = summarize_results(results, config["success_threshold"])
    output_dir = tmp_path / "saved" / f"{dimension}d"
    assert save_results(results, summary, config, output_dir) == output_dir
    payload = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert payload == {"config": config, "summary": summary}
    with (output_dir / "runs.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == len(results) == 2
    assert sum(row["success"] == "True" for row in rows) == summary["successful_runs"]
    with np.load(output_dir / "trajectories.npz", allow_pickle=False) as saved:
        assert saved.files == ["run_001", "run_002"]
        for row, result in zip(rows, results):
            assert int(row["seed"]) == result["seed"]
            assert row["status"] == result["status"]
            assert float(row["final_value"]) == result["best_value"]
            for key in ["iterations_completed", "function_evaluations", "gradient_evaluations"]:
                assert int(row[key]) == result[key]
            initial_point = [float(row[f"initial_x{i + 1}"]) for i in range(dimension)]
            final_point = [float(row[f"final_x{i + 1}"]) for i in range(dimension)]
            np.testing.assert_array_equal(initial_point, result["initial_point"])
            np.testing.assert_array_equal(final_point, result["best_solution"])
            np.testing.assert_array_equal(saved[row["run_id"]], result["trajectory"])
    if dimension == 3:
        assert rows[1]["status"] == "diverged"
        assert rows[1]["success"] == "False"
        assert rows[1]["final_value"] == "inf"
        assert results[0]["trajectory"].shape != results[1]["trajectory"].shape
        failed_config = dict(config, runs=1, seed=43)
        failed_results = [results[1]]
        failed_summary = summarize_results(failed_results, config["success_threshold"])
        save_results(failed_results, failed_summary, failed_config, output_dir)
        payload = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
        assert payload["summary"]["mean_value"] is None
        with np.load(output_dir / "trajectories.npz", allow_pickle=False) as saved:
            assert saved.files == ["run_001"]
            np.testing.assert_array_equal(saved["run_001"], failed_results[0]["trajectory"])
        with (output_dir / "runs.csv").open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        assert len(rows) == 1
        assert rows[0]["seed"] == "43"
