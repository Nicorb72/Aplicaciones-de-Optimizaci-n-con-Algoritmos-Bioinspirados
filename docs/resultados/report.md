# Parte 1: comparación de costos y resultados

Fuente de las tablas y figuras: elaboración propia. Este informe se genera desde las corridas, no desde números escritos a mano.

Umbral(es) de éxito: **0.0001**. Intervalo(s) de semillas: **42–71**.

## Metodología y alcance

Cada configuración y su umbral están conservados en `comparison.json`; las versiones ejecutadas, en `environment.json`. Las semillas son `seed + i`, para i desde 0 hasta runs−1. El éxito exige terminar con valor finito y f ≤ umbral. La desviación estándar es muestral (ddof=1). Media, desviación, mejor y peor excluyen divergencias; la tasa de éxito y los promedios de costos incluyen TODAS las corridas. Una divergencia nunca cuenta como éxito.

GD entrega el valor de su último punto; los heurísticos entregan el mejor conocido. Los intervalos del YAML definen el muestreo inicial. Los heurísticos recortan posiciones a esos intervalos; GD no aplica proyección. Es una diferencia de tratamiento de límites que debe considerarse al interpretar resultados.

## Tabla 1. Valores finales y éxito

Esta tabla contiene **16 configuraciones** (una fila por función, dimensión y método).

| Función   | Dim. | Método      | Corridas |       Media | Desv. muestral |       Mejor |        Peor | Éxito | Excluidas |
| ---------- | ---: | ------------ | -------: | ----------: | -------------: | ----------: | ----------: | -----: | --------: |
| rastrigin  |    2 | de           |       30 |           0 |              0 |           0 |           0 | 100.0% |         0 |
| rastrigin  |    2 | evolutionary |       30 |     0.49748 |       0.569466 |           0 |     1.98992 |  53.3% |         0 |
| rastrigin  |    2 | gd           |       30 |     15.8197 |        10.2047 |    0.994959 |     31.8385 |   0.0% |         0 |
| rastrigin  |    2 | pso          |       30 |           0 |              0 |           0 |           0 | 100.0% |         0 |
| rastrigin  |    3 | de           |       30 |           0 |              0 |           0 |           0 | 100.0% |         0 |
| rastrigin  |    3 | evolutionary |       30 |     1.65826 |        1.97844 | 1.12976e-12 |     9.94956 |  23.3% |         0 |
| rastrigin  |    3 | gd           |       30 |     24.4758 |        14.4054 |     1.98992 |     53.7273 |   0.0% |         0 |
| rastrigin  |    3 | pso          |       30 |    0.165827 |       0.458808 |           0 |     1.98992 |  86.7% |         0 |
| rosenbrock |    2 | de           |       30 |           0 |              0 |           0 |           0 | 100.0% |         0 |
| rosenbrock |    2 | evolutionary |       30 |  5.1852e-08 |    6.75591e-08 | 3.69447e-11 | 2.23949e-07 | 100.0% |         0 |
| rosenbrock |    2 | gd           |       30 | 2.79564e-05 |    1.63826e-05 | 2.63701e-10 | 6.56467e-05 | 100.0% |         0 |
| rosenbrock |    2 | pso          |       30 |           0 |              0 |           0 |           0 | 100.0% |         0 |
| rosenbrock |    3 | de           |       30 | 1.43248e-19 |    3.02453e-19 |  7.1335e-22 |  1.4938e-18 | 100.0% |         0 |
| rosenbrock |    3 | evolutionary |       30 | 0.000462552 |     0.00100442 | 2.79018e-07 |  0.00536461 |  40.0% |         0 |
| rosenbrock |    3 | gd           |       30 | 1.16142e-05 |    7.44872e-06 | 1.92243e-07 | 3.89182e-05 |  90.0% |         3 |
| rosenbrock |    3 | pso          |       30 | 4.46107e-08 |     4.8878e-08 | 1.86357e-10 | 1.76139e-07 | 100.0% |         0 |

## Tabla 2. Costo medio por corrida

Esta tabla contiene **16 configuraciones**, las mismas de la Tabla 1.

Se cuentan las llamadas de optimización a $f$ y al gradiente por separado. Las evaluaciones para dibujar quedan fuera. Definimos $C = N_f + 2dN_{\mathrm{grad}}$: diferencias centrales necesitarían $2d$ llamadas a $f$ por gradiente. Es una convención de equivalencia, NO el tiempo real ni el costo medido del gradiente analítico implementado. La Tabla 2 muestra los contadores medios obtenidos con los parámetros guardados en comparison.json. GD incluye la evaluación final de $f$. PSO y DE usan 40000 evaluaciones de $f$; el evolutivo usa 63976 porque conserva el 20% de una población de 40 y genera 32 hijos durante 1998 generaciones. Los resultados de cada dimensión se analizan por separado.

| Función   | Dim. | Método      | N_f medio | N_grad medio | C medio |
| ---------- | ---: | ------------ | --------: | -----------: | ------: |
| rastrigin  |    2 | de           |     40000 |            0 |   40000 |
| rastrigin  |    2 | evolutionary |     63976 |            0 |   63976 |
| rastrigin  |    2 | gd           |         1 |        10000 |   40001 |
| rastrigin  |    2 | pso          |     40000 |            0 |   40000 |
| rastrigin  |    3 | de           |     40000 |            0 |   40000 |
| rastrigin  |    3 | evolutionary |     63976 |            0 |   63976 |
| rastrigin  |    3 | gd           |         1 |        10000 |   60001 |
| rastrigin  |    3 | pso          |     40000 |            0 |   40000 |
| rosenbrock |    2 | de           |     40000 |            0 |   40000 |
| rosenbrock |    2 | evolutionary |     63976 |            0 |   63976 |
| rosenbrock |    2 | gd           |         1 |        10000 |   40001 |
| rosenbrock |    2 | pso          |     40000 |            0 |   40000 |
| rosenbrock |    3 | de           |     40000 |            0 |   40000 |
| rosenbrock |    3 | evolutionary |     63976 |            0 |   63976 |
| rosenbrock |    3 | gd           |         1 |      9000.83 |   54006 |
| rosenbrock |    3 | pso          |     40000 |            0 |   40000 |

Las divergencias pueden reducir el costo medio de GD porque detienen la corrida: ese menor costo no representa una mejora. Si se cambian los parámetros o se usa la configuración de demostración, los presupuestos anteriores ya no tienen por qué coincidir; la Tabla 2 siempre muestra los costos realmente contados bajo la convención elegida.

## Discusión

**Rastrigin 2D.** DE: 30/30 éxitos, media 0; Evolutivo: 16/30 éxitos, media 0.49748; GD: 0/30 éxitos, media 15.8197; PSO: 30/30 éxitos, media 0.
El menor promedio observado entre las configuraciones mostradas corresponde a DE, PSO. Es una descripción de esta muestra y estos parámetros, no una garantía de superioridad general.
Rastrigin tiene muchos mínimos locales. GD es un método local, mientras que la exploración poblacional permite comparar distintas regiones sin garantizar el mínimo global.

**Rastrigin 3D.** DE: 30/30 éxitos, media 0; Evolutivo: 7/30 éxitos, media 1.65826; GD: 0/30 éxitos, media 24.4758; PSO: 26/30 éxitos, media 0.165827.
El menor promedio observado entre las configuraciones mostradas corresponde a DE. Es una descripción de esta muestra y estos parámetros, no una garantía de superioridad general.
Rastrigin tiene muchos mínimos locales. GD es un método local, mientras que la exploración poblacional permite comparar distintas regiones sin garantizar el mínimo global.

**Rosenbrock 2D.** DE: 30/30 éxitos, media 0; Evolutivo: 30/30 éxitos, media 5.1852e-08; GD: 30/30 éxitos, media 2.79564e-05; PSO: 30/30 éxitos, media 0.
El menor promedio observado entre las configuraciones mostradas corresponde a DE, PSO. Es una descripción de esta muestra y estos parámetros, no una garantía de superioridad general.
Rosenbrock tiene un valle curvo y estrecho: GD aprovecha el gradiente, pero un paso fijo puede avanzar lentamente por el valle o divergir. PSO, DE y el evolutivo exploran mediante poblaciones sin calcular derivadas.

**Rosenbrock 3D.** DE: 30/30 éxitos, media 1.43248e-19; Evolutivo: 12/30 éxitos, media 0.000462552; GD: 27/30 éxitos, media 1.16142e-05; PSO: 30/30 éxitos, media 4.46107e-08.
El menor promedio observado entre las configuraciones mostradas corresponde a DE. Es una descripción de esta muestra y estos parámetros, no una garantía de superioridad general.
Rosenbrock tiene un valle curvo y estrecho: GD aprovecha el gradiente, pero un paso fijo puede avanzar lentamente por el valle o divergir. PSO, DE y el evolutivo exploran mediante poblaciones sin calcular derivadas.

El evolutivo conserva soluciones mediante elitismo, selecciona padres por torneo, genera descendencia con cruce BLX-alpha y aplica mutación gaussiana con recorte al dominio permitido. Los parámetros exactos se conservan en comparison.json. Estos mecanismos combinan conservación de buenas soluciones y exploración, aunque no garantizan alcanzar el mínimo global en todas las corridas. PSO combina memoria individual y colectiva. DE usa diferencias entre individuos para proponer candidatos y conserva las mejoras. Igualar el costo proxy no iguala los mecanismos de búsqueda ni prueba que el tiempo de ejecución sea igual.

Antes del experimento principal se realizó un Grid Search exploratorio en 3D con tres semillas y 10000 evaluaciones por configuración. Después se seleccionaron configuraciones prometedoras y se validaron con 30 corridas y semillas 42–71. No se realizaron pruebas de significancia. Las conclusiones se limitan a estas funciones, dimensiones, semillas, umbral y presupuestos. La configuración principal compara los cuatro métodos en 2D y 3D; cada dimensión se interpreta por separado. Un valor calculado como cero refleja precisión finita; no demuestra que todas las coordenadas sean exactamente el óptimo en aritmética real.

La selección mediante Grid Search se justifica por el número reducido de hiperparámetros y su reproducibilidad. Bergstra y Bengio (2012) señalan que Random Search puede ser más eficiente cuando solo algunos hiperparámetros son influyentes; por ello los valores elegidos no se presentan como óptimos universales.

## Parámetros seleccionados

Los valores de esta tabla son la configuración consolidada después del Grid Search exploratorio y la validación final. Se aplican a Rosenbrock y Rastrigin en ambas dimensiones.

| Método   | Parámetros usados                                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------- |
| PSO       | partículas=40, iteraciones=999, w=0.7, c1=1.4, c2=1.0                                                     |
| Evolutivo | población=40, generaciones=1998, torneo=3, alpha=0.6, mutación=0.5, sigma=0.1, élite=0.2 (8 individuos) |
| DE        | población=40, generaciones=999, F=0.7, CR=0.5                                                             |
| GD        | iteraciones=10000, tasa de aprendizaje según configuración                                               |

La selección se documenta con mayor detalle en [Justificacion de parametros](<../Justificacion%20de%20parametros.md>). La referencia empleada es Bergstra, J., & Bengio, Y. (2012). *Random Search for Hyper-Parameter Optimization*. JMLR, 13, 281–305.

## Figuras y animaciones

Las curvas muestran corridas completadas y finitas. La trayectoria ilustrada es la primera exitosa o, si no hay éxitos, la primera completada. Es una selección explícita para ilustrar, no una corrida representativa de toda la distribución. En heurísticos, la línea une mejores puntos conocidos: no es la trayectoria de una partícula individual. En PSO, los puntos lavanda del GIF sí muestran las posiciones guardadas de todas las partículas.

La [Figura 1](../../results/part1/figures/rastrigin/de/2d/convergence.png) muestra convergencia de rastrigin 2D con DE. Fuente: elaboración propia.

La [Figura 2](../../results/part1/figures/rastrigin/de/2d/trajectory.png) muestra trayectoria de rastrigin 2D con DE. Fuente: elaboración propia.

[Animación de rastrigin/de/2d](../../results/part1/animations/rastrigin/de/2d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 3](../../results/part1/figures/rastrigin/evolutionary/2d/convergence.png) muestra convergencia de rastrigin 2D con EVOLUTIONARY. Fuente: elaboración propia.

La [Figura 4](../../results/part1/figures/rastrigin/evolutionary/2d/trajectory.png) muestra trayectoria de rastrigin 2D con EVOLUTIONARY. Fuente: elaboración propia.

[Animación de rastrigin/evolutionary/2d](../../results/part1/animations/rastrigin/evolutionary/2d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 5](../../results/part1/figures/rastrigin/gd/2d/convergence.png) muestra convergencia de rastrigin 2D con GD. Fuente: elaboración propia.

La [Figura 6](../../results/part1/figures/rastrigin/gd/2d/trajectory.png) muestra trayectoria de rastrigin 2D con GD. Fuente: elaboración propia.

[Animación de rastrigin/gd/2d](../../results/part1/animations/rastrigin/gd/2d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 7](../../results/part1/figures/rastrigin/pso/2d/convergence.png) muestra convergencia de rastrigin 2D con PSO. Fuente: elaboración propia.

La [Figura 8](../../results/part1/figures/rastrigin/pso/2d/trajectory.png) muestra trayectoria de rastrigin 2D con PSO. Fuente: elaboración propia.

[Animación de rastrigin/pso/2d](../../results/part1/animations/rastrigin/pso/2d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 9](../../results/part1/figures/rastrigin/de/3d/convergence.png) muestra convergencia de rastrigin 3D con DE. Fuente: elaboración propia.

La [Figura 10](../../results/part1/figures/rastrigin/de/3d/trajectory.png) muestra trayectoria de rastrigin 3D con DE. Fuente: elaboración propia.

[Animación de rastrigin/de/3d](../../results/part1/animations/rastrigin/de/3d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 11](../../results/part1/figures/rastrigin/evolutionary/3d/convergence.png) muestra convergencia de rastrigin 3D con EVOLUTIONARY. Fuente: elaboración propia.

La [Figura 12](../../results/part1/figures/rastrigin/evolutionary/3d/trajectory.png) muestra trayectoria de rastrigin 3D con EVOLUTIONARY. Fuente: elaboración propia.

[Animación de rastrigin/evolutionary/3d](../../results/part1/animations/rastrigin/evolutionary/3d/trajectory_run_002.gif). Fuente: elaboración propia.

La [Figura 13](../../results/part1/figures/rastrigin/gd/3d/convergence.png) muestra convergencia de rastrigin 3D con GD. Fuente: elaboración propia.

La [Figura 14](../../results/part1/figures/rastrigin/gd/3d/trajectory.png) muestra trayectoria de rastrigin 3D con GD. Fuente: elaboración propia.

[Animación de rastrigin/gd/3d](../../results/part1/animations/rastrigin/gd/3d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 15](../../results/part1/figures/rastrigin/pso/3d/convergence.png) muestra convergencia de rastrigin 3D con PSO. Fuente: elaboración propia.

La [Figura 16](../../results/part1/figures/rastrigin/pso/3d/trajectory.png) muestra trayectoria de rastrigin 3D con PSO. Fuente: elaboración propia.

[Animación de rastrigin/pso/3d](../../results/part1/animations/rastrigin/pso/3d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 17](../../results/part1/figures/rosenbrock/de/2d/convergence.png) muestra convergencia de rosenbrock 2D con DE. Fuente: elaboración propia.

La [Figura 18](../../results/part1/figures/rosenbrock/de/2d/trajectory.png) muestra trayectoria de rosenbrock 2D con DE. Fuente: elaboración propia.

[Animación de rosenbrock/de/2d](../../results/part1/animations/rosenbrock/de/2d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 19](../../results/part1/figures/rosenbrock/evolutionary/2d/convergence.png) muestra convergencia de rosenbrock 2D con EVOLUTIONARY. Fuente: elaboración propia.

La [Figura 20](../../results/part1/figures/rosenbrock/evolutionary/2d/trajectory.png) muestra trayectoria de rosenbrock 2D con EVOLUTIONARY. Fuente: elaboración propia.

[Animación de rosenbrock/evolutionary/2d](../../results/part1/animations/rosenbrock/evolutionary/2d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 21](../../results/part1/figures/rosenbrock/gd/2d/convergence.png) muestra convergencia de rosenbrock 2D con GD. Fuente: elaboración propia.

La [Figura 22](../../results/part1/figures/rosenbrock/gd/2d/trajectory.png) muestra trayectoria de rosenbrock 2D con GD. Fuente: elaboración propia.

[Animación de rosenbrock/gd/2d](../../results/part1/animations/rosenbrock/gd/2d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 23](../../results/part1/figures/rosenbrock/pso/2d/convergence.png) muestra convergencia de rosenbrock 2D con PSO. Fuente: elaboración propia.

La [Figura 24](../../results/part1/figures/rosenbrock/pso/2d/trajectory.png) muestra trayectoria de rosenbrock 2D con PSO. Fuente: elaboración propia.

[Animación de rosenbrock/pso/2d](../../results/part1/animations/rosenbrock/pso/2d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 25](../../results/part1/figures/rosenbrock/de/3d/convergence.png) muestra convergencia de rosenbrock 3D con DE. Fuente: elaboración propia.

La [Figura 26](../../results/part1/figures/rosenbrock/de/3d/trajectory.png) muestra trayectoria de rosenbrock 3D con DE. Fuente: elaboración propia.

[Animación de rosenbrock/de/3d](../../results/part1/animations/rosenbrock/de/3d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 27](../../results/part1/figures/rosenbrock/evolutionary/3d/convergence.png) muestra convergencia de rosenbrock 3D con EVOLUTIONARY. Fuente: elaboración propia.

La [Figura 28](../../results/part1/figures/rosenbrock/evolutionary/3d/trajectory.png) muestra trayectoria de rosenbrock 3D con EVOLUTIONARY. Fuente: elaboración propia.

[Animación de rosenbrock/evolutionary/3d](../../results/part1/animations/rosenbrock/evolutionary/3d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 29](../../results/part1/figures/rosenbrock/gd/3d/convergence.png) muestra convergencia de rosenbrock 3D con GD. Fuente: elaboración propia.

La [Figura 30](../../results/part1/figures/rosenbrock/gd/3d/trajectory.png) muestra trayectoria de rosenbrock 3D con GD. Fuente: elaboración propia.

[Animación de rosenbrock/gd/3d](../../results/part1/animations/rosenbrock/gd/3d/trajectory_run_001.gif). Fuente: elaboración propia.

La [Figura 31](../../results/part1/figures/rosenbrock/pso/3d/convergence.png) muestra convergencia de rosenbrock 3D con PSO. Fuente: elaboración propia.

La [Figura 32](../../results/part1/figures/rosenbrock/pso/3d/trajectory.png) muestra trayectoria de rosenbrock 3D con PSO. Fuente: elaboración propia.

[Animación de rosenbrock/pso/3d](../../results/part1/animations/rosenbrock/pso/3d/trajectory_run_001.gif). Fuente: elaboración propia.

[Fundamentación matemática, ecuaciones y referencias](../parte1_metodologia.md).
