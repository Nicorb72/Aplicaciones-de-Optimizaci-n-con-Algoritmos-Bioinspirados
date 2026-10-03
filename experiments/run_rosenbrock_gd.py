from optimization.gradient_descent_rosenbrock import run_gradient_descent_rosenbrock


if __name__ == "__main__":
    result = run_gradient_descent_rosenbrock([-1.2, 1.0])
    print(result)
