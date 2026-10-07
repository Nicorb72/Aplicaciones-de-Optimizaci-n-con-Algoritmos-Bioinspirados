import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image
import pytest
import yaml

from experiments.run_part1 import configurations
from optimization.benchmark import FUNCTIONS, METHODS, run_configuration
from optimization.rosenbrock import rosenbrock
from visualization.animations import rosenbrock_isosurface


@pytest.mark.parametrize("name", ["rosenbrock", "rastrigin"])
@pytest.mark.parametrize("method", ["pso", "evolutionary", "de"])
@pytest.mark.parametrize("dimension", [2, 3])
def test_population_counts_history_and_reproducibility(name, method, dimension):
    calls = []
    def objective(point):
        calls.append(point.copy())
        return FUNCTIONS[name](point)
    kwargs = {"particles": 5, "iterations": 4} if method == "pso" else {"population_size": 5, "generations": 4}
    result = METHODS[method](objective, [(-2, 2)] * dimension, seed=17, **kwargs)
    assert result["function_evaluations"] == len(calls) == (17 if method == "evolutionary" else 25)
    assert result["gradient_evaluations"] == 0
    assert result["iterations_completed"] == 4
    assert result["trajectory"].shape == (5, dimension)
    assert np.all(np.diff(result["value_history"]) <= 0)
    np.testing.assert_allclose(result["value_history"], [FUNCTIONS[name](x) for x in result["trajectory"]])
    assert result["evaluation_history"][-1] == len(calls)
    assert np.all(np.array(calls) >= -2) and np.all(np.array(calls) <= 2)
    repeated = METHODS[method](FUNCTIONS[name], [(-2, 2)] * dimension, seed=17, **kwargs)
    np.testing.assert_array_equal(result["trajectory"], repeated["trajectory"])
    if method == "pso":
        assert result["population_history"].shape == (5, 5, dimension)
        np.testing.assert_array_equal(np.array(calls).reshape(5, 5, dimension), result["population_history"])


@pytest.mark.parametrize("level", [1, 10])
def test_isosurfaces_are_actual_rosenbrock_level_sets(level):
    X, Y = np.meshgrid(np.linspace(0.6, 1.2, 40), np.linspace(0.4, 1.5, 40))
    for Z in rosenbrock_isosurface(X, Y, level):
        valid = np.isfinite(Z)
        assert np.count_nonzero(valid) > 10
        points = np.column_stack([X[valid], Y[valid], Z[valid]])
        np.testing.assert_allclose([rosenbrock(p) for p in points], level, rtol=1e-12, atol=1e-12)


def short_suite(tmp_path):
    config = yaml.safe_load(Path("configs/part1.yaml").read_text())
    config.update(runs=30, output_dir=str(tmp_path / "results"))
    config["methods"] = {"gd": {"iterations": 3}, "pso": {"particles": 4, "iterations": 3},
                         "evolutionary": {"population_size": 4, "generations": 3}, "de": {"population_size": 4, "generations": 3}}
    config["animation"] = {"frames": 3, "fps": 10}
    return config


def test_suite_covers_requirements_and_equivalent_budget():
    suite = yaml.safe_load(Path("configs/part1.yaml").read_text())
    configs = list(configurations(suite))
    assert len(configs) == 10
    assert all(c["runs"] >= 30 for c in configs)
    assert {(c["function"], c["method"]) for c in configs} == {(f, m) for f in FUNCTIONS for m in ["gd", *METHODS]}
    methods = suite["methods"]
    assert 1 + 4 * methods["gd"]["iterations"] == 40001
    assert methods["pso"]["particles"] * (methods["pso"]["iterations"] + 1) == 40000
    assert methods["de"]["population_size"] * (methods["de"]["generations"] + 1) == 40000
    p = methods["evolutionary"]["population_size"]
    assert p + (p - p // 2) * methods["evolutionary"]["generations"] == 40000


def test_all_configurations_keep_costs_and_independent_seeds(tmp_path):
    for config in configurations(short_suite(tmp_path)):
        results, summary = run_configuration(config)
        assert [r["seed"] for r in results] == list(range(42, 72))
        assert np.unique([r["initial_point"] for r in results], axis=0).shape[0] == 30
        assert summary["runs"] == 30
        cost = [r["function_evaluations"] + 2 * config["dimension"] * r["gradient_evaluations"] for r in results]
        assert summary["mean_equivalent_evaluations"] == np.mean(cost)
        assert sum(r["status"] == "completed" and r["best_value"] <= config["success_threshold"] for r in results) == summary["successful_runs"]


def test_cli_runs_and_renders_pso_from_saved_data(tmp_path):
    config = short_suite(tmp_path)
    path = tmp_path / "suite.yaml"
    path.write_text(yaml.safe_dump(config))
    env = dict(os.environ, MPLBACKEND="Agg")
    base = [sys.executable, "-m", "experiments.run_part1", "--config", str(path)]
    p = subprocess.run(base + ["--no-visuals"], env=env, capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, p.stdout + p.stderr
    output = Path(config["output_dir"])
    assert len(json.loads((output / "comparisons/all/comparison.json").read_text())) == 10
    originals = {p: p.read_bytes() for p in (output / "raw").rglob('*') if p.is_file()}
    p = subprocess.run(base + ["--render-only", "--method", "pso", "--function", "rastrigin"], env=env, capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, p.stdout + p.stderr
    assert originals == {p: p.read_bytes() for p in originals}
    gifs = list((output / "animations/rastrigin/pso/2d").glob('*.gif'))
    assert len(gifs) == 1
    with Image.open(gifs[0]) as gif:
        assert gif.n_frames == 3
    assert (output / "figures/rastrigin/pso/2d/convergence.png").exists()
    # Un cambio de parámetros no puede reutilizar silenciosamente resultados viejos.
    config["methods"]["pso"]["iterations"] = 4
    path.write_text(yaml.safe_dump(config))
    p = subprocess.run(base + ["--render-only", "--method", "pso", "--function", "rastrigin"], env=env, capture_output=True, text=True, timeout=60)
    assert p.returncode != 0 and "no coincide" in p.stderr


def test_rastrigin_command_no_longer_depends_on_ignored_code(tmp_path):
    config = yaml.safe_load(Path("configs/rastrigin.yaml").read_text())
    config.update(iterations=3, output_dir=str(tmp_path / "rastrigin"))
    path = tmp_path / "rastrigin.yaml"
    path.write_text(yaml.safe_dump(config))
    p = subprocess.run([sys.executable, "-m", "experiments.run_rastrigin_gd", "--config", str(path),
                        "--frames", "2", "--figures-dir", str(tmp_path / 'figures'),
                        "--animations-dir", str(tmp_path / 'animations')],
                       env=dict(os.environ, MPLBACKEND="Agg"), capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, p.stdout + p.stderr
    for dimension in (2, 3):
        data = json.loads((tmp_path / f'rastrigin/{dimension}d/summary.json').read_text())
        assert data['summary']['runs'] == 30
        assert data['summary']['mean_gradient_evaluations'] == 3
        with Image.open(tmp_path / f'animations/{dimension}d/trajectory_run_001.gif') as gif:
            assert gif.n_frames == 2
