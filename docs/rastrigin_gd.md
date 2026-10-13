# Rastrigin con descenso por gradiente (GD)

**Autor:** Ivan Dario Gomez Cabrera

**Implementación:** `src/optimization/gradient_descent_rastrigin.py`
(`run_gradient_descent_rastrigin`). El experimento independiente se ejecuta con
`experiments/run_rastrigin_gd.py`; los resultados presentados aquí corresponden
a las corridas consolidadas del proyecto para Rastrigin en 2D y 3D.

## Objetivo

Evaluar el descenso por gradiente (GD, *Gradient Descent*) al minimizar la
función de Rastrigin en dos y tres dimensiones. Rastrigin es una función
multimodal: tiene numerosos mínimos locales y un mínimo global en el origen.
Esta característica permite observar que un método basado en gradientes puede
converger a un mínimo local dependiendo de su punto de inicio.

## Función de Rastrigin

Para un vector de dimensión \(d\), la función utilizada es:

\[
f(\mathbf{x}) = 10d + \sum_{i=1}^{d}
\left(x_i^2 - 10\cos(2\pi x_i)\right).
\]

El mínimo global es \(f(\mathbf{0}) = 0\), alcanzado en
\(\mathbf{x} = \mathbf{0}\). El gradiente analítico implementado es:

\[
\frac{\partial f}{\partial x_i}
= 2x_i + 20\pi\sin(2\pi x_i), \qquad i=1,\ldots,d.
\]

## Cómo funciona GD

GD actualiza el punto de búsqueda en la dirección opuesta al gradiente:

\[
\mathbf{x}_{t+1}
= \mathbf{x}_t - \eta \nabla f(\mathbf{x}_t),
\]

donde \(\eta\) es la tasa de aprendizaje. En cada iteración el algoritmo evalúa
el gradiente analítico y guarda el punto en la trayectoria. Al finalizar,
evalúa la función en el último punto y devuelve ese valor. No mantiene un
enjambre ni una población, y no conserva el mejor punto visitado: su resultado
es el punto final de la trayectoria.

## Configuración del experimento

Los parámetros están definidos en `configs/rastrigin.yaml`. Para cada
dimensión se hacen 30 corridas con puntos iniciales muestreados uniformemente
en el dominio. La semilla base es 42 y las corridas usan las semillas 42 a 71,
lo que permite reproducir los inicios aleatorios.

| Parámetro | Valor |
| --- | ---: |
| Dominio de inicialización | \([-5.12, 5.12]\) por coordenada |
| Dimensiones | 2 y 3 |
| Tasa de aprendizaje (`learning_rate`) | 0.001 |
| Iteraciones (`iterations`) | 10 000 |
| Corridas por dimensión (`runs`) | 30 |
| Semilla base (`seed`) | 42 |
| Umbral de éxito | \(f(\mathbf{x}) \le 0.0001\) |

El dominio se utiliza para generar los puntos iniciales. GD no proyecta ni
recorta las posiciones durante la búsqueda, por lo que las iteraciones
posteriores pueden salir de ese intervalo.

## Resultados

Se considera exitosa una corrida si termina con un valor finito menor o igual
al umbral de \(0.0001\). La media, desviación estándar, mejor y peor valor se
calculan sobre los valores finales de las corridas completadas; las tasas de
éxito consideran las 30 corridas.

| Dimensión | Corridas | Media final | Desv. estándar muestral | Mejor | Peor | Éxito |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2D | 30 | 15.8197 | 10.2047 | 0.994959 | 31.8385 | 0 % |
| 3D | 30 | 24.4758 | 14.4054 | 1.98992 | 53.7273 | 0 % |

No hubo corridas divergentes en estas configuraciones. Aunque algunas
trayectorias alcanzaron valores relativamente bajos, ninguna terminó dentro
del umbral de éxito. El mejor resultado en ambas dimensiones es mayor que
cero, lo que concuerda con la dificultad de escapar de los mínimos locales de
Rastrigin usando únicamente un descenso local basado en el gradiente. En 3D,
el mayor número de coordenadas también aumenta las posibilidades de terminar
en una combinación de mínimos locales.

## Figuras y trayectorias

Las imágenes y animaciones siguientes se generaron para GD sobre Rastrigin.
En las figuras de trayectoria se representa el recorrido de una corrida; las
de convergencia muestran cómo cambia el valor de la función a través de las
iteraciones.

### Rastrigin en 2D

- [Trayectoria 2D](imagenes/part1/figures/rastrigin/gd/2d/trajectory.png)
- [Convergencia 2D](imagenes/part1/figures/rastrigin/gd/2d/convergence.png)
- [Animación de la trayectoria 2D](imagenes/part1/animations/rastrigin/gd/2d/trajectory_run_001.gif)

### Rastrigin en 3D

- [Trayectoria 3D](imagenes/part1/figures/rastrigin/gd/3d/trajectory.png)
- [Convergencia 3D](imagenes/part1/figures/rastrigin/gd/3d/convergence.png)
- [Animación de la trayectoria 3D](imagenes/part1/animations/rastrigin/gd/3d/trajectory_run_001.gif)

## Costo de las corridas

Cada corrida ejecuta 10 000 evaluaciones del gradiente analítico y una
evaluación final de la función objetivo. Para comparar el costo entre métodos,
el proyecto usa la convención \(C = N_f + 2dN_{\text{grad}}\), que estima
cuántas evaluaciones de la función requeriría aproximar cada gradiente con
diferencias centrales. No representa el tiempo real de ejecución ni el costo
de calcular el gradiente analítico:

| Dimensión | Evaluaciones de \(f\) | Evaluaciones del gradiente | Costo equivalente \(C\) |
| ---: | ---: | ---: | ---: |
| 2D | 1 | 10 000 | 40 001 |
| 3D | 1 | 10 000 | 60 001 |

## Cómo ejecutar

Desde la raíz del repositorio, con las dependencias instaladas en el entorno
Python activo:

```bash
python -m experiments.run_rastrigin_gd
```

El comando utiliza `configs/rastrigin.yaml` y genera resultados, gráficas y
animaciones en las carpetas `results/raw/rastrigin_gd/`,
`results/figures/rastrigin_gd/` y `results/animations/rastrigin_gd/`,
respectivamente.

Los resultados consolidados y la metodología general se pueden consultar en
[el informe de comparación](resultados/report.md) y en
[comparison.json](resultados/comparison.json).
