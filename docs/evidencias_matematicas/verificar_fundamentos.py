"""Verificaciones numéricas de las derivaciones publicadas en el blog.

Ejecutar desde la raíz: python docs/evidencias_matematicas/verificar_fundamentos.py
El conteo de mínimos de Rastrigin es numérico, sobre la caja del experimento.
"""
from pathlib import Path
import hashlib
import json
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from optimization.rosenbrock import rosenbrock, rosenbrock_gradient
from optimization.rastrigin import rastrigin, rastrigin_gradient


def verify():
    rng = np.random.default_rng(123)
    checks = []
    for name, objective, gradient, low, high in [
        ('rosenbrock', rosenbrock, rosenbrock_gradient, -2, 2),
        ('rastrigin', rastrigin, rastrigin_gradient, -5.12, 5.12),
    ]:
        for dimension in (2, 3):
            max_error = 0.0
            for point in rng.uniform(low, high, size=(20, dimension)):
                numeric = np.zeros(dimension)
                for j in range(dimension):
                    step = np.eye(dimension)[j] * 1e-6
                    numeric[j] = (objective(point + step) - objective(point - step)) / 2e-6
                analytic = gradient(point)
                error = np.max(np.abs(analytic - numeric) / np.maximum(1, np.abs(numeric)))
                max_error = max(max_error, float(error))
                np.testing.assert_allclose(analytic, numeric, rtol=1e-5, atol=1e-5)
            optimum = np.ones(dimension) if name == 'rosenbrock' else np.zeros(dimension)
            assert objective(optimum) == 0
            checks.append({'function': name, 'dimension': dimension, 'points': 20,
                           'max_scaled_gradient_error': max_error})

    hessian = np.array([[802., -400.], [-400., 200.]])
    eigenvalues = np.linalg.eigvalsh(hessian)
    assert np.all(eigenvalues > 0)
    # Estacionariedad en 3D: el segundo factor tiene mínimo 51 en x=-1/2.
    assert 200 * (-0.5)**2 + 200 * (-0.5) + 101 == 51

    def first(x): return 2*x + 20*np.pi*np.sin(2*np.pi*x)
    def second(x): return 2 + 40*np.pi**2*np.cos(2*np.pi*x)
    grid = np.linspace(-5.12, 5.12, 40001)
    roots = []
    for left, right in zip(grid[:-1], grid[1:]):
        if first(left) == 0:
            roots.append(float(left))
        elif first(left) * first(right) < 0:
            a, b = left, right
            for _ in range(60):
                mid = (a + b) / 2
                if first(a) * first(mid) <= 0:
                    b = mid
                else:
                    a = mid
            roots.append(float((a + b) / 2))
    roots = sorted(set(round(x, 12) for x in roots))
    minima = [x for x in roots if second(x) > 0]
    assert len(roots) == 21 and len(minima) == 11
    assert max(abs(first(x)) for x in roots) < 1e-8
    files = [ROOT/'src/optimization/rosenbrock.py', ROOT/'src/optimization/rastrigin.py']
    return {
        'seed': 123, 'finite_difference_step': 1e-6, 'gradient_checks': checks,
        'rosenbrock_2d': {'hessian_at_minimum': hessian.tolist(), 'eigenvalues': eigenvalues.tolist(),
                          'condition_number': float(eigenvalues[-1]/eigenvalues[0]),
                          'quadratic_local_step_upper_bound': float(2/eigenvalues[-1])},
        'rosenbrock_3d': {'stationary_polynomial': '(x1-1)(200*x1^2+200*x1+101)=0',
                          'quadratic_factor_minimum': 51, 'only_stationary_point': [1,1,1]},
        'rastrigin': {'interval': [-5.12,5.12], 'grid_points': len(grid),
                      'stationary_points_1d': roots, 'strict_minima_1d': minima,
                      'local_minima_count_2d': len(minima)**2, 'local_minima_count_3d': len(minima)**3,
                      'condition_number_at_origin': 1,
                      'scope': 'Conteo numérico por aislamiento de cambios de signo y bisección, con segunda derivada positiva; no es una certificación simbólica exhaustiva.'},
        'source_sha256': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
    }


if __name__ == '__main__':
    result = verify()
    output = Path(__file__).with_name('fundamentos_verificados.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print('Gradientes, mínimos conocidos, Hessiana y conteo numérico comprobados.')
    print(output)
