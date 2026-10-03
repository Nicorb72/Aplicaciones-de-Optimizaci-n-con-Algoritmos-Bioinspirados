import matplotlib.pyplot as plt
import numpy as np

from optimization.rastrigin import rastrigin


def plot_rastrigin():
    x = np.linspace(-5.12, 5.12, 200)
    y = np.linspace(-5.12, 5.12, 200)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[rastrigin([xi, yi]) for xi in x] for yi in y])
    plt.contourf(X, Y, Z, levels=50)
    plt.title("Rastrigin")
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    plot_rastrigin()
