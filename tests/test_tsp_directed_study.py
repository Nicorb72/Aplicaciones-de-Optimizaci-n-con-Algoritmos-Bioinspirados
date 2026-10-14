"""Regresiones del TSP asimétrico, semillas emparejadas y archivo de costos."""
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np
import pytest

from tsp.ant_colony import run_ant_colony_tsp
from tsp.cost_model import calculate_tour_cost, compute_total_cost_matrix, load_tsp_data
from experiments.run_tsp import run_hourly_rate_study, tour_edges
from scripts.export_tsp_costs import export_costs

ROOT = Path(__file__).resolve().parents[1]


def test_aco_reinforces_only_travelled_direction_including_closure():
    matrix = np.array([[0., 1., 12.], [8., 0., 2.], [3., 9., 0.]])
    q, rho = 2., .25
    result = run_ant_colony_tsp(matrix, n_ants=1, iterations=1, q=q, rho=rho, seed=7)
    edges = tour_edges(result["best_tour"])
    assert result["best_cost"] == calculate_tour_cost(result["best_tour"], matrix)
    initial = (1-rho) / (3 * matrix[matrix > 0].mean())
    for u, v in edges:
        assert result["pheromone_matrix"][u, v] == pytest.approx(initial + 3*q/result["best_cost"])
        assert result["pheromone_matrix"][v, u] == pytest.approx(initial)
    np.testing.assert_allclose(np.diag(result["pheromone_matrix"]), initial)
    assert tour_edges([0, 1, 2]) == tour_edges([1, 2, 0])
    assert tour_edges([0, 1, 2]) != tour_edges([0, 2, 1])


def test_hourly_changes_compare_same_seed_and_preserve_all_runs(monkeypatch):
    import experiments.run_tsp as module
    def fake(config, hourly_rate):
        # A different winning seed between rates must not imply a paired route change.
        tours = {42: [0, 1, 2], 43: [0, 2, 1]}
        cost = (10 if config['seed'] == 42 else 20) if hourly_rate == 0 else (30 if config['seed'] == 42 else 25)
        return {"best_tour": tours[config['seed']], "best_cost": cost,
                "breakdown": {"total_distance_km": 3, "total_time_hours": 2}}
    monkeypatch.setattr(module, 'run_single_tsp', fake)
    rows = run_hourly_rate_study({'method': 'aco'}, [10, 0, 10], [42, 43])
    assert [r['hourly_rate'] for r in rows] == [0, 10]
    assert rows[0]['best_seed'] != rows[1]['best_seed']
    assert rows[1]['changed_seeds_vs_previous'] == 0
    assert rows[1]['previous_hourly_rate'] == 0
    assert rows[1]['mean_cost_eur'] == 27.5
    assert rows[1]['std_cost_eur'] == pytest.approx(np.std([30, 25], ddof=1))
    assert all(len(r['runs']) == 2 for r in rows)


def test_export_matches_independent_components_and_records_hashes(tmp_path):
    for name in ('matrices.npz', 'vehicle_specs.yaml', 'spain_capitals.csv'):
        shutil.copy2(ROOT / 'data/tsp' / name, tmp_path / name)
    meta = export_costs(tmp_path, hourly_rate=17, toll_multiplier=2)
    data = load_tsp_data(tmp_path)
    with np.load(tmp_path / 'total_cost_matrix.npz') as stored:
        expected = 17*data['times_hours'] + 2*data['tolls_eur'] + meta['consumption_l_per_100km']/100*meta['fuel_price_eur_per_l']*data['distances_km']
        np.fill_diagonal(expected, 0)
        np.testing.assert_allclose(stored['total_cost_eur'], expected)
        np.testing.assert_allclose(stored['total_cost_eur'], sum(stored[k] for k in ('time_cost_eur', 'fuel_cost_eur', 'toll_cost_eur')))
    assert meta['output_sha256'] == hashlib.sha256((tmp_path/'total_cost_matrix.npz').read_bytes()).hexdigest()
    assert len(meta['city_order']) == 47
    assert json.loads((tmp_path/'total_cost_matrix_metadata.json').read_text(encoding='utf-8')) == meta
    assert not np.array_equal(expected, compute_total_cost_matrix())


def test_committed_base_matrix_is_current():
    directory = ROOT/'data/tsp'
    meta = json.loads((directory/'total_cost_matrix_metadata.json').read_text(encoding='utf-8'))
    for name, sha in meta['input_sha256'].items():
        assert hashlib.sha256((directory/name).read_bytes()).hexdigest() == sha
    assert hashlib.sha256((directory/meta['output_file']).read_bytes()).hexdigest() == meta['output_sha256']
    with np.load(directory/meta['output_file']) as stored:
        np.testing.assert_allclose(stored['total_cost_eur'], compute_total_cost_matrix())
