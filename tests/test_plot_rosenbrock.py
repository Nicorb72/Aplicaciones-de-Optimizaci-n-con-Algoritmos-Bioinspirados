import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pytest
import yaml

from experiments.run_rosenbrock_gd import run_experiments
from optimization.result_storage import save_results
from optimization.statistics import summarize_results
from visualization.plot_rosenbrock import plot_rosenbrock


@pytest.mark.parametrize(
    "dimension, seed, runs, domain, expected_figures",
    [
        (2, 42, 2, {"lower": -2, "upper": 2}, 2),
        (3, 42, 2, {"lower": -2, "upper": 2}, 2),
        (3, 43, 1, {"lower": -2, "upper": 2}, 1),
        (2, 42, 1, {"lower": 1, "upper": 1}, 2),
    ],
)
def test_plots_saved_runs_without_changing_data(tmp_path, monkeypatch, dimension, seed, runs, domain, expected_figures):
    config = {
        "function": "rosenbrock", "dimension": dimension, "domain": domain,
        "learning_rate": 0.001, "iterations": 10, "runs": runs, "seed": seed,
        "success_threshold": 0.0001,
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    results = run_experiments(config_path)
    summary = summarize_results(results, config["success_threshold"])
    raw_dir = save_results(results, summary, config, tmp_path / "raw")
    original_data = {path.name: path.read_bytes() for path in raw_dir.iterdir()}

    def forbid_optimization(*args, **kwargs):
        raise AssertionError("La visualización no debe ejecutar GD.")

    monkeypatch.setattr("experiments.run_rosenbrock_gd.run_gradient_descent_rosenbrock", forbid_optimization)
    paths = plot_rosenbrock(raw_dir, tmp_path / "figures")
    assert len(paths) == expected_figures
    for path in paths:
        pixels = mpimg.imread(path)
        assert pixels.shape[0] > 100 and pixels.shape[1] > 100
        assert np.std(pixels[:, :, :3]) > 0
    assert {path.name: path.read_bytes() for path in raw_dir.iterdir()} == original_data
    assert not plt.get_fignums()
    with pytest.raises(ValueError, match="corrida completada"):
        plot_rosenbrock(raw_dir, tmp_path / "figures", run_id="run_999")
