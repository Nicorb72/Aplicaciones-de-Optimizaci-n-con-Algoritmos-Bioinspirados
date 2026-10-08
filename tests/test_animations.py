import json

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pytest
import yaml

from experiments.run_rosenbrock_gd import run_experiments
from optimization.result_storage import save_results
from optimization.statistics import summarize_results
from visualization import animations


@pytest.mark.parametrize("iterations, frames", [(10, 4), (2, 20), (0, 10)])
@pytest.mark.parametrize("dimension", [2, 3])
def test_gif_preserves_endpoints_and_saved_data(tmp_path, monkeypatch, iterations, frames, dimension):
    config = {
        "function": "rosenbrock", "dimension": dimension,
        "domain": {"lower": -2, "upper": 2},
        "learning_rate": 0.001, "iterations": iterations, "runs": 1,
        "seed": 42, "success_threshold": 0.0001,
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    results = run_experiments(config_path)
    summary = summarize_results(results, config["success_threshold"])
    raw_dir = save_results(results, summary, config, tmp_path / "raw")
    original_data = {path.name: path.read_bytes() for path in raw_dir.iterdir()}
    observed = []
    original_animation = animations.FuncAnimation

    def record_animation(fig, update, **kwargs):
        def record_update(index):
            artists = update(index)
            point = artists[1].get_data() if dimension == 2 else artists[1].get_data_3d()
            line = artists[0].get_data() if dimension == 2 else artists[0].get_data_3d()
            observed.append((index, np.array(point).reshape(dimension), np.array(line).T.copy()))
            return artists
        return original_animation(fig, record_update, **kwargs)

    def forbid_optimization(*args, **kwargs):
        raise AssertionError("La animación no debe ejecutar GD.")

    monkeypatch.setattr(animations, "FuncAnimation", record_animation)
    monkeypatch.setattr("experiments.run_rosenbrock_gd.run_gradient_descent_rosenbrock", forbid_optimization)
    path = animations.animate_rosenbrock(raw_dir, tmp_path / "gifs", frames=frames, fps=10)
    with Image.open(path) as gif:
        assert gif.format == "GIF"
        assert gif.n_frames == min(frames, iterations + 1)
        assert gif.info["duration"] == 100
        gif.seek(gif.n_frames - 1)
        assert gif.size == (1000, 650)
    assert observed[0][0] == 0
    assert observed[-1][0] == iterations
    assert path.parent.name == f"{dimension}d"
    for index, point, line in observed:
        np.testing.assert_array_equal(point, results[0]["trajectory"][index])
        np.testing.assert_array_equal(line, results[0]["trajectory"][:index + 1])
    assert {path.name: path.read_bytes() for path in raw_dir.iterdir()} == original_data
    assert not plt.get_fignums()
    with pytest.raises(ValueError, match="corrida completada"):
        animations.animate_rosenbrock(raw_dir, tmp_path / "gifs", run_id="run_999")


@pytest.mark.parametrize("option, value", [("frames", 1), ("frames", 1.5), ("fps", 0), ("fps", 101)])
def test_gif_rejects_invalid_parameters(tmp_path, option, value):
    with pytest.raises(ValueError, match=option):
        animations.animate_rosenbrock(tmp_path, tmp_path, **{option: value})


def test_gif_rejects_unsupported_dimension(tmp_path):
    (tmp_path / "summary.json").write_text(json.dumps({"config": {"dimension": 4}}), encoding="utf-8")
    with pytest.raises(ValueError, match="2D"):
        animations.animate_rosenbrock(tmp_path, tmp_path)


def test_movement_pacing_spends_time_on_large_displacements():
    trajectory = np.array([[0., 0.], [10., 0.], [10.01, 0.], [10.02, 0.]])
    positions = animations.animation_positions(trajectory, 60, 'movement')
    assert len(positions) == 60
    assert positions[0] == 0 and positions[-1] == 3
    assert np.all(np.diff(positions) > 0)
    # La primera actualización recorre casi toda la distancia: debe verse lentamente.
    assert np.count_nonzero(positions < 1) > 50
    np.testing.assert_array_equal(animations.interpolate_position(trajectory, .5), [5., 0.])
    np.testing.assert_array_equal(animations.interpolate_position(trajectory, 3), trajectory[-1])
    # Aunque el mejor conocido no cambie, el enjambre sí puede estar moviéndose.
    stationary_best = np.zeros_like(trajectory)
    swarm = trajectory[:, None, :]
    np.testing.assert_allclose(positions, animations.animation_positions(stationary_best, 60, 'movement', swarm))
    still = animations.animation_positions(stationary_best, 60, 'movement')
    np.testing.assert_allclose(still, np.linspace(0, 3, 60))


@pytest.mark.parametrize('dimension', [2, 3])
def test_movement_gif_interpolates_without_changing_saved_results(tmp_path, monkeypatch, dimension):
    config = {'function': 'rosenbrock', 'dimension': dimension, 'domain': {'lower': -2, 'upper': 2},
              'learning_rate': .001, 'iterations': 3, 'runs': 1, 'seed': 42, 'success_threshold': .0001}
    path = tmp_path / 'config.yaml'
    path.write_text(yaml.safe_dump(config))
    results = run_experiments(path)
    raw = save_results(results, summarize_results(results, .0001), config, tmp_path / 'raw')
    original = {p.name: p.read_bytes() for p in raw.iterdir()}
    trajectory = results[0]['trajectory']
    observed = []
    original_animation = animations.FuncAnimation

    def record_animation(fig, update, **kwargs):
        def record(position):
            artists = update(position)
            data = artists[1].get_data() if dimension == 2 else artists[1].get_data_3d()
            observed.append((position, np.array(data).reshape(dimension)))
            return artists
        return original_animation(fig, record, **kwargs)

    monkeypatch.setattr(animations, 'FuncAnimation', record_animation)
    gif_path = animations.animate_saved(raw, tmp_path / 'gifs', frames=12, fps=5, pacing='movement')
    with Image.open(gif_path) as gif:
        assert gif.n_frames == 12  # Puede haber más fotogramas que iteraciones guardadas.
        duration = 0
        for frame in range(gif.n_frames):
            gif.seek(frame)
            duration += gif.info['duration']
        assert duration == 2400
    assert observed[0][0] == 0 and observed[-1][0] == 3
    assert any(position != int(position) for position, _ in observed)
    for position, point in observed:
        left = int(position)
        right = min(left + 1, len(trajectory) - 1)
        weight = position - left
        expected = (1 - weight) * trajectory[left] + weight * trajectory[right]
        np.testing.assert_allclose(point, expected)
    assert original == {p.name: p.read_bytes() for p in raw.iterdir()}
    assert not plt.get_fignums()
