import numpy as np
import pytest

from optimization.statistics import summarize_results


def test_summary_matches_known_values_and_keeps_failures_in_denominator():
    results = [
        {"status": "completed", "best_value": 1.0},
        {"status": "completed", "best_value": 2.0},
        {"status": "completed", "best_value": 3.0},
        {"status": "diverged", "best_value": 0.0},
        {"status": "diverged", "best_value": np.inf},
        {"status": "completed", "best_value": np.nan},
    ]
    summary = summarize_results(results, success_threshold=2.0)
    assert summary == {
        "runs": 6,
        "completed_runs": 4,
        "diverged_runs": 2,
        "included_runs": 3,
        "excluded_runs": 3,
        "success_threshold": 2.0,
        "successful_runs": 2,
        "success_rate": 2 / 6,
        "mean_value": 2.0,
        "std_value": 1.0,
        "best_value": 1.0,
        "worst_value": 3.0,
    }


def test_summary_with_all_runs_diverged():
    results = [
        {"status": "diverged", "best_value": np.inf},
        {"status": "diverged", "best_value": np.nan},
    ]
    summary = summarize_results(results, success_threshold=0.0001)
    assert summary["included_runs"] == 0
    assert summary["excluded_runs"] == summary["diverged_runs"] == 2
    assert summary["successful_runs"] == summary["success_rate"] == 0
    for key in ["mean_value", "std_value", "best_value", "worst_value"]:
        assert summary[key] is None


def test_summary_with_one_value_has_no_sample_standard_deviation():
    summary = summarize_results(
        [{"status": "completed", "best_value": 0.0001}], success_threshold=0.0001
    )
    assert summary["mean_value"] == summary["best_value"] == summary["worst_value"] == 0.0001
    assert summary["std_value"] is None
    assert summary["success_rate"] == 1.0


def test_summary_rejects_empty_results():
    with pytest.raises(ValueError, match="al menos una corrida"):
        summarize_results([], success_threshold=0.0001)


@pytest.mark.parametrize("threshold", [-1.0, np.inf, np.nan])
def test_summary_rejects_invalid_threshold(threshold):
    with pytest.raises(ValueError, match="finito y no negativo"):
        summarize_results([{"status": "completed", "best_value": 0.0}], threshold)
