import csv
import json
from pathlib import Path

import numpy as np


def save_results(results, summary, config, output_dir):
    """Guarda las corridas, su resumen y las trayectorias sin recalcular la función."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    dimension = config["dimension"]
    fields = [
        "run_id", "seed", "status", "success", "final_value",
        "iterations_completed", "function_evaluations", "gradient_evaluations", "equivalent_evaluations",
    ]
    fields += [f"initial_x{i + 1}" for i in range(dimension)]
    fields += [f"final_x{i + 1}" for i in range(dimension)]
    trajectories = {}
    with (output_dir / "runs.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for index, result in enumerate(results, start=1):
            run_id = f"run_{index:03d}"
            row = {
                "run_id": run_id,
                "seed": result["seed"],
                "status": result["status"],
                "success": bool(
                    result["status"] == "completed"
                    and np.isfinite(result["best_value"])
                    and result["best_value"] <= summary["success_threshold"]
                ),
                "final_value": result["best_value"],
                "iterations_completed": result["iterations_completed"],
                "function_evaluations": result["function_evaluations"],
                "gradient_evaluations": result["gradient_evaluations"],
                "equivalent_evaluations": result["function_evaluations"] + 2 * dimension * result["gradient_evaluations"],
            }
            row.update({f"initial_x{i + 1}": value for i, value in enumerate(result["initial_point"])})
            row.update({f"final_x{i + 1}": value for i, value in enumerate(result["best_solution"])})
            writer.writerow(row)
            trajectories[run_id] = result["trajectory"]
    with (output_dir / "summary.json").open("w", encoding="utf-8") as file:
        json.dump({"config": config, "summary": summary}, file, indent=2, ensure_ascii=False, allow_nan=False)
        file.write("\n")
    np.savez_compressed(output_dir / "trajectories.npz", **trajectories)
    for field, filename in [("value_history", "values.npz"), ("evaluation_history", "evaluations.npz"),
                            ("population_history", "populations.npz")]:
        histories = {f"run_{i:03d}": result[field] for i, result in enumerate(results, 1) if field in result}
        path = output_dir / filename
        if histories:
            np.savez_compressed(path, **histories)
        elif path.exists():
            path.unlink()  # Elimina únicamente un historial generado que quedó obsoleto.
    return output_dir
