import numpy as np

from .rastrigin import rastrigin, rastrigin_gradient


def run_gradient_descent_rastrigin(punto_inicial, learning_rate=1e-3, i=1000):
    x = np.asarray(punto_inicial, dtype=float).copy()
    trayectoria = [x.copy()]
    funcion_de_evaluacion = 0
    Evaluacion_del_gradiante = 0
    estado = "completado"
    for _ in range(i):
        with np.errstate(over="ignore", invalid="ignore"):
            grad = rastrigin_gradient(x)
            Evaluacion_del_gradiante += 1
            next_x = x - learning_rate * grad
        if not np.all(np.isfinite(grad)) or not np.all(np.isfinite(next_x)):
            estado = "divergieron"
            break
        x = next_x
        trayectoria.append(x.copy())
    with np.errstate(over="ignore", invalid="ignore"):
        valor_final = float(rastrigin(x))
    funcion_de_evaluacion += 1
    if not np.isfinite(valor_final):
        estado = "divergieron"
    return {
        "Mejor_solucion": x,
        "Mejor_valor": valor_final,
        "trayectoria": np.asarray(trayectoria),
        "funcion_de_evaluacion": funcion_de_evaluacion,
        "Evaluacion_del_gradiante": Evaluacion_del_gradiante,
        "estado": estado,
        "iteraciones_completadas": len(trayectoria) - 1,
    }
