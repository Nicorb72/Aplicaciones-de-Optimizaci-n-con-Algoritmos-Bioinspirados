from optimization.pso import run_pso
from optimization.rastrigin import rastrigin


if __name__ == "__main__":
    result = run_pso(rastrigin, [(-5.12, 5.12), (-5.12, 5.12)])
    print(result)
