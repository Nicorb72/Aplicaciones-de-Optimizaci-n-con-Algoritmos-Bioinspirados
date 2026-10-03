import matplotlib.pyplot as plt
import numpy as np

from optimization.rosenbrock import rosenbrock


def plot_rosenbrock():
    x = np.linspace(-2, 2, 200)
    y = np.linspace(-1, 3, 200)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[rosenbrock([xi, yi]) for xi in x] for yi in y])
    plt.contourf(X, Y, Z, levels=50)
    plt.title("Rosenbrock")
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    plot_rosenbrock()
