import numpy as np
import pytest
import yaml

from experiments.run_rosenbrock_gd import run_experiment, run_experiments
from optimization.rosenbrock import rosenbrock_gradient


@pytest.mark.parametrize("dimension", [2, 3])
def test_random_experiment_uses_config_and_repeats_with_seed(tmp_path, dimension):
    config = {
        "function": "rosenbrock",
        "dimension": dimension,
        "domain": {"lower": -1.0, "upper": 1.0},
        "learning_rate": 0.0001,
        "iterations": 3,
        "seed": 42,
    }
    config_path = tmp_path / "rosenbrock.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    first = run_experiment(config_path)
    repeated = run_experiment(config_path)
    x0 = first["initial_point"]
    assert x0.shape == (dimension,)
    assert np.all((x0 >= -1.0) & (x0 < 1.0))
    assert first["seed"] == 42
    assert first["trajectory"].shape == (4, dimension)
    np.testing.assert_array_equal(first["trajectory"][0], x0)
    np.testing.assert_allclose(
        first["trajectory"][1], x0 - config["learning_rate"] * rosenbrock_gradient(x0)
    )
    np.testing.assert_array_equal(first["trajectory"], repeated["trajectory"])
    assert first["best_value"] == repeated["best_value"]
    config["seed"] = 43
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    different = run_experiment(config_path)
    assert not np.array_equal(x0, different["initial_point"])


def test_experiment_rejects_other_function(tmp_path):
    config_path = tmp_path / "other.yaml"
    config_path.write_text("function: rastrigin\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Rosenbrock"):
        run_experiment(config_path)


@pytest.mark.parametrize("dimension", [2, 3])
def test_multiple_runs_are_separate_and_reproducible(tmp_path, dimension):
    config = {
        "function": "rosenbrock",
        "dimension": dimension,
        "domain": {"lower": -1.0, "upper": 1.0},
        "learning_rate": 0.0001,
        "iterations": 3,
        "runs": 30,
        "seed": 42,
    }
    config_path = tmp_path / "rosenbrock.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    results = run_experiments(config_path)
    repeated = run_experiments(config_path)
    assert len(results) == 30
    assert [result["seed"] for result in results] == list(range(42, 72))
    initial_points = np.array([result["initial_point"] for result in results])
    assert np.unique(initial_points, axis=0).shape[0] == 30
    for result, repeat in zip(results, repeated):
        assert result["trajectory"].shape == (4, dimension)
        np.testing.assert_array_equal(result["trajectory"][0], result["initial_point"])
        np.testing.assert_array_equal(result["trajectory"], repeat["trajectory"])
        assert result["best_value"] == repeat["best_value"]
        assert result["function_evaluations"] == 1
        assert result["gradient_evaluations"] == 3
    assert not np.shares_memory(results[0]["trajectory"], results[1]["trajectory"])


@pytest.mark.parametrize("runs", [0, -1, 1.5, True])
def test_multiple_runs_reject_invalid_count(tmp_path, runs):
    config_path = tmp_path / "invalid.yaml"
    config_path.write_text(yaml.safe_dump({"runs": runs}), encoding="utf-8")
    with pytest.raises(ValueError, match="entero positivo"):
        run_experiments(config_path)
