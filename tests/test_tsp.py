"""Pruebas unitarias para los datos y algoritmos de la Parte 2 (TSP España)."""

import numpy as np
import pytest

from tsp.cost_model import compute_total_cost_matrix, load_tsp_data, calculate_tour_cost, get_tour_breakdown
from tsp.ant_colony import run_ant_colony_tsp
from tsp.genetic_tsp import run_genetic_tsp


def test_spain_capitals_loaded_correctly():
    data = load_tsp_data()
    capitals = data["capitals"]
    assert len(capitals) == 47, f"Deben ser exactamente 47 capitales peninsulares, se encontraron {len(capitals)}"
    for c in capitals:
        assert -10.0 <= c["lon"] <= 5.0
        assert 35.0 <= c["lat"] <= 45.0


def test_cost_matrix_dimensions_and_diagonal():
    matrix = compute_total_cost_matrix(hourly_rate=25.0)
    assert matrix.shape == (47, 47)
    assert np.all(np.diag(matrix) == 0.0)
    assert np.all(matrix >= 0.0)
    assert np.all(np.isfinite(matrix))


def test_ant_colony_returns_valid_permutation():
    cost_matrix = compute_total_cost_matrix(hourly_rate=25.0)
    result = run_ant_colony_tsp(
        cost_matrix=cost_matrix,
        n_ants=5,
        iterations=2,
        seed=123,
    )
    tour = result["best_tour"]
    assert len(tour) == 47
    assert set(tour) == set(range(47)), "El tour debe ser una permutación exacta de las 47 ciudades"
    assert result["best_cost"] > 0
    assert len(result["cost_history"]) == 2


def test_genetic_algorithm_returns_valid_permutation():
    cost_matrix = compute_total_cost_matrix(hourly_rate=25.0)
    result = run_genetic_tsp(
        cost_matrix=cost_matrix,
        population_size=10,
        generations=3,
        seed=123,
    )
    tour = result["best_tour"]
    assert len(tour) == 47
    assert set(tour) == set(range(47)), "El tour debe ser una permutación exacta de las 47 ciudades"
    assert result["best_cost"] > 0
    assert len(result["cost_history"]) == 4  # gen 0 + 3 gens


def test_tour_breakdown_consistency():
    tour = np.arange(47)
    breakdown = get_tour_breakdown(tour, hourly_rate=25.0)
    total = breakdown["time_cost_eur"] + breakdown["toll_cost_eur"] + breakdown["fuel_cost_eur"]
    assert np.isclose(breakdown["total_cost_eur"], total)
    assert breakdown["total_distance_km"] > 0
    assert breakdown["total_time_hours"] > 0
