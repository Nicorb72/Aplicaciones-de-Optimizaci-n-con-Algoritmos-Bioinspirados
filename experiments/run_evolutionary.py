from optimization.evolutionary import run_evolutionary
from optimization.rastrigin import rastrigin


if __name__ == "__main__":
    result = run_evolutionary(rastrigin, [(-5.12, 5.12), (-5.12, 5.12)])
    print(result)
