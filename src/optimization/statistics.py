import numpy as np


def summarize_results(results, success_threshold):
    """Resume valores finales completados y finitos; el éxito usa todas las corridas."""
    if not results:
        raise ValueError("Se necesita al menos una corrida para calcular estadísticas.")
    if not np.isfinite(success_threshold) or success_threshold < 0:
        raise ValueError("El umbral de éxito debe ser finito y no negativo.")
    values = np.array([
        result["best_value"] for result in results
        if result["status"] == "completed" and np.isfinite(result["best_value"])
    ], dtype=float)
    total = len(results)
    included = len(values)
    successful = int(np.count_nonzero(values <= success_threshold))
    return {
        "runs": total,
        "completed_runs": sum(result["status"] == "completed" for result in results),
        "diverged_runs": sum(result["status"] == "diverged" for result in results),
        "included_runs": included,
        "excluded_runs": total - included,
        "success_threshold": float(success_threshold),
        "successful_runs": successful,
        "success_rate": successful / total,
        "mean_value": float(np.mean(values)) if included else None,
        "std_value": float(np.std(values, ddof=1)) if included > 1 else None,
        "best_value": float(np.min(values)) if included else None,
        "worst_value": float(np.max(values)) if included else None,
    }
