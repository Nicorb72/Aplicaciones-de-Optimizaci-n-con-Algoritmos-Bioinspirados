import numpy as np
import pytest

from tsp.cost_model import compute_total_cost_matrix, calculate_tour_cost, get_tour_breakdown
from experiments.run_toll_study import run_study, directed_edges


def test_toll_multiplier_affects_only_toll_component():
    zero = compute_total_cost_matrix(toll_multiplier=0)
    base = compute_total_cost_matrix()
    double = compute_total_cost_matrix(toll_multiplier=2)
    np.testing.assert_allclose(double - base, base - zero)
    np.testing.assert_array_equal(base, compute_total_cost_matrix(toll_multiplier=1))
    tour = [0, 28, 36] + [i for i in range(47) if i not in {0, 28, 36}]
    for factor, matrix in [(0, zero), (1, base), (2, double)]:
        bd = get_tour_breakdown(tour, toll_multiplier=factor)
        assert np.isclose(bd['total_cost_eur'], calculate_tour_cost(tour, matrix))
        assert np.isclose(bd['total_cost_eur'], sum(bd[k] for k in ('fuel_cost_eur', 'time_cost_eur', 'toll_cost_eur')))
        if factor == 0:
            assert bd['toll_cost_eur'] == 0


@pytest.mark.parametrize('factor', [-1, float('nan'), float('inf')])
def test_invalid_multiplier_rejected(factor):
    with pytest.raises(ValueError):
        compute_total_cost_matrix(toll_multiplier=factor)
    with pytest.raises(ValueError):
        get_tour_breakdown(range(47), toll_multiplier=factor)


def test_matched_seed_study_preserves_directed_routes_and_fixed_costs():
    configs = [{'method':'aco','n_ants':3,'iterations':2},
               {'method':'ga','population_size':10,'generations':3}]
    study = run_study(configs, [42, 43])
    assert len(study['runs']) == 12 and len(study['summaries']) == 6
    for row in study['runs']:
        base = next(r for r in study['runs'] if r['method']==row['method'] and r['seed']==row['seed'] and r['toll_multiplier']==1)
        matrix = compute_total_cost_matrix(toll_multiplier=row['toll_multiplier'])
        assert set(row['tour']) == set(range(47))
        assert np.isclose(row['best_cost_eur'], calculate_tour_cost(row['tour'], matrix))
        assert np.isclose(row['base_tour_cost_in_scenario_eur'], calculate_tour_cost(base['tour'], matrix))
        if row['toll_multiplier']==1:
            assert row['directed_edges_changed_vs_base']==0
    assert directed_edges([0,1,2]) == directed_edges([1,2,0])
    assert directed_edges([0,1,2]) != directed_edges([0,2,1])
