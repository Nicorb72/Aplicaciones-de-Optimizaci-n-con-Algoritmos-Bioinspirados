from optimization.differential_evolution import run_differential_evolution
from optimization.rastrigin import rastrigin


if __name__ == "__main__":
    result = run_differential_evolution(rastrigin, [(-5.12, 5.12), (-5.12, 5.12)])
    print(result)
