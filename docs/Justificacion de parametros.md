# Justificación de parámetros

## 1. Propósito

Los hiperparámetros de los algoritmos no se eligieron únicamente por
intuición. Primero se realizó una búsqueda sistemática mediante **Grid Search**
para comparar combinaciones de valores previamente definidos. Después se
seleccionaron las configuraciones más prometedoras y se ejecutaron con el
presupuesto completo y las semillas del experimento principal. Los valores que
se utilizan oficialmente son los que aparecen en los archivos YAML de
`configs/`.

Este procedimiento separa dos objetivos:

1. **Exploración:** encontrar regiones razonables del espacio de
   hiperparámetros con un presupuesto reducido.
2. **Validación:** medir las configuraciones seleccionadas con más corridas y
   un presupuesto de búsqueda mayor antes de compararlas en el informe final.

La selección no significa que exista un conjunto universalmente óptimo. Los
resultados dependen de la función, la dimensión, el dominio, las semillas, el
presupuesto y el criterio de éxito.

## 2. Por qué se utilizó Grid Search

Grid Search evalúa el producto cartesiano de listas discretas de valores. Es
una estrategia transparente y reproducible: cada combinación queda definida de
antemano, se puede repetir con las mismas semillas y permite explicar por qué
se descartaron o conservaron determinados valores.

La referencia principal es:

> Bergstra, J., & Bengio, Y. (2012). *Random Search for Hyper-Parameter
> Optimization*. **Journal of Machine Learning Research, 13**, 281–305.
> https://jmlr.org/papers/v13/bergstra12a.html

Bergstra y Bengio presentan Grid Search como el método estándar y muestran que
Random Search puede ser más eficiente cuando solo algunos hiperparámetros
influyen realmente en el rendimiento. Por tanto, Grid Search es razonable en
este proyecto porque:

- el número de hiperparámetros explorados es pequeño;
- cada parámetro tiene una lista corta y explícita de valores;
- se necesita una justificación fácil de auditar en una entrega académica;
- las combinaciones se pueden repetir con las mismas semillas;
- el experimento permite comparar configuraciones bajo un presupuesto fijo.

La limitación es el crecimiento combinatorio. Por ejemplo, una grilla con
cinco parámetros y tres valores por parámetro requiere
\(3^5=243\) configuraciones. Por eso la búsqueda se realizó con presupuestos
exploratorios menores y no con el presupuesto completo de todas las corridas.

## 3. Protocolo de búsqueda

Para la Parte 1, la búsqueda exploratoria del cuaderno
`Nootebooks/Optimización.ipynb` utilizó:

- funciones Rosenbrock y Rastrigin en 3D;
- tres semillas: 42, 43 y 44;
- 10 000 evaluaciones de la función por configuración;
- el mismo presupuesto dentro de cada algoritmo;
- ordenamiento principal por el menor valor medio final;
- desempate por la tasa de éxito y la desviación observada.

El presupuesto exploratorio se mantuvo fijo de la siguiente forma:

| Método | Presupuesto exploratorio |
|---|---:|
| PSO | 20 partículas × 500 evaluaciones por generación/estado = 10 000 |
| Evolutivo | 20 individuos + 10 hijos × 998 generaciones = 10 000 |
| DE | 20 individuos × 500 evaluaciones por generación/estado = 10 000 |

Después de la exploración se tomaron configuraciones representativas y se
validaron en el experimento principal. La configuración principal utiliza
30 corridas por configuración, semillas 42–71 y 40 000 evaluaciones para los
métodos poblacionales. GD se mide con el costo equivalente
\(N_f+2dN_{\nabla}\).

## 4. Hiperparámetros seleccionados para la Parte 1

La siguiente tabla transcribe los valores efectivos de
`configs/part1.yaml`. Estos son los valores usados para generar los resultados
de `results/part1/`.

| Método | Hiperparámetro | Valor seleccionado | Función de uso |
|---|---|---:|---|
| GD | `iterations` | 10000 | Presupuesto de iteraciones |
| GD | `learning_rate` | 0.001 | Tasa definida por función |
| PSO | `particles` | 40 | Tamaño del enjambre |
| PSO | `iterations` | 999 | Presupuesto del enjambre |
| PSO | `inertia` | 0.7 | Persistencia de la velocidad |
| PSO | `cognitive` | 1.4 | Influencia de la mejor posición individual |
| PSO | `social` | 1.0 | Influencia de la mejor posición colectiva |
| Evolutivo | `population_size` | 40 | Tamaño de la población |
| Evolutivo | `generations` | 1998 | Presupuesto generacional |
| Evolutivo | `tournament_size` | 3 | Presión de selección |
| Evolutivo | `crossover_alpha` | 0.6 | Amplitud del cruce BLX-\(\alpha\) |
| Evolutivo | `mutation_rate` | 0.5 | Probabilidad de mutar una coordenada |
| Evolutivo | `mutation_sigma` | 0.1 | Desviación de la mutación gaussiana |
| Evolutivo | `elite_fraction` | 0.2 | Fracción conservada por elitismo |
| DE | `population_size` | 40 | Tamaño de la población |
| DE | `generations` | 999 | Presupuesto generacional |
| DE | `f` | 0.7 | Factor de escala diferencial |
| DE | `cr` | 0.5 | Probabilidad de cruce |

Los valores de `domain` y `learning_rate` se mantienen por función:

| Función | Dominio por coordenada | `learning_rate` de GD | Mínimo global |
|---|---|---:|---|
| Rosenbrock | \([-2,2]\) | 0.001 | \(f=0\) en \((1,\ldots,1)\) |
| Rastrigin | \([-5.12,5.12]\) | 0.001 | \(f=0\) en \((0,\ldots,0)\) |

Los métodos poblacionales se ejecutan tanto en 2D como en 3D. La misma
configuración de hiperparámetros se conserva entre dimensiones para que la
comparación sea reproducible; la dimensión cambia el paisaje y el número de
coordenadas, no se introduce una ventaja por reajuste posterior.

## 5. Resultado de la exploración de la Parte 1

La grilla exploratoria reportada en el cuaderno encontró, entre otras, las
siguientes configuraciones destacadas en 3D:

| Método | Función | Valores exploratorios destacados |
|---|---|---|
| PSO | Rastrigin | `inertia=0.7`, `cognitive=1.4`, `social=1.0` |
| PSO | Rosenbrock | `inertia=0.7`, `cognitive=1.0`, `social=1.4` |
| Evolutivo | Rastrigin | `tournament_size=3`, `crossover_alpha=0.0`, `mutation_rate=0.5`, `mutation_sigma=0.1`, `elite_fraction=0.5` |
| Evolutivo | Rosenbrock | `tournament_size=2`, `crossover_alpha=0.6`, `mutation_rate=0.75`, `mutation_sigma=0.2`, `elite_fraction=0.5` |
| DE | Rastrigin | `f=0.5`, `cr=0.5` |
| DE | Rosenbrock | `f=0.7`, `cr=0.9` |

La búsqueda mostró que una configuración ganadora puede depender de la
función. Para el experimento de producción se necesitaba una configuración
única y trazable por método, aplicable a ambas funciones y dimensiones. Por
eso los YAML finales representan una selección consolidada, no una afirmación
de que los mismos valores sean óptimos para cada función por separado.

En particular, la selección final del evolutivo usa
`crossover_alpha=0.6`, `mutation_rate=0.5`, `mutation_sigma=0.1` y
`elite_fraction=0.2`. Estos valores deben interpretarse como la configuración
validada en producción, mientras que las filas de la tabla anterior son
resultados de la fase exploratoria del cuaderno.

## 6. Hiperparámetros seleccionados para TSP

La búsqueda de TSP utilizó presupuestos reducidos y fijos para que todas las
combinaciones de un mismo algoritmo fueran comparables. Se evaluaron
27 configuraciones de GA y 81 configuraciones de ACO, con semillas 42, 43 y
44. Las configuraciones ganadoras se validaron y se conservaron en los YAML
finales.

### Algoritmo genético

| Parámetro | Valor seleccionado | Papel |
|---|---:|---|
| `population_size` | 100 | Tamaño de la población final |
| `generations` | 250 | Número de generaciones |
| `mutation_rate` | 0.5 | Probabilidad de mutación |
| `tournament_size` | 6 | Tamaño del torneo |
| `elite_size` | 2 | Individuos conservados |

Estos valores corresponden a `configs/tsp_ga.yaml`. La grilla exploratoria
identificó `mutation_rate=0.50`, `tournament_size=6` y `elite_size=2` como la
mejor combinación bajo el presupuesto reducido.

### Colonia de hormigas

| Parámetro | Valor seleccionado | Papel |
|---|---:|---|
| `n_ants` | 25 | Número de hormigas |
| `iterations` | 80 | Iteraciones finales |
| `alpha` | 1.0 | Influencia de feromona |
| `beta` | 2.5 | Influencia heurística |
| `rho` | 0.25 | Tasa de evaporación |
| `q` | 100.0 | Intensidad del depósito |

Estos valores corresponden a `configs/tsp_aco.yaml`. La grilla exploratoria
identificó `alpha=0.50`, `beta=4.0`, `rho=0.05` y `q=200.0` como la mejor
combinación bajo el presupuesto reducido. Los valores finales del YAML son la
configuración consolidada usada en la ejecución final.

## 7. Cómo se interpretan las tablas de resultados

La selección se considera favorable cuando combina:

- menor valor medio de la función objetivo;
- mayor tasa de éxito frente al umbral;
- baja dispersión entre semillas;
- ausencia de divergencias;
- presupuesto comparable entre métodos.

No se usa únicamente la mejor corrida, porque una solución aislada puede ser
producto de una semilla favorable. Por eso el informe principal conserva la
media, la desviación estándar, el mejor y el peor valor, la tasa de éxito y
los costos medios.

Las configuraciones del Grid Search son exploratorias y las configuraciones
de los YAML son las que deben utilizarse para interpretar el benchmark final.
No se deben mezclar directamente las medias de la grilla con las medias de las
30 corridas principales: tienen distinto número de semillas y distinto
presupuesto.

## 8. Limitaciones y mejoras posibles

Grid Search es apropiado aquí por la cantidad reducida de parámetros, pero
puede desperdiciar evaluaciones en combinaciones poco influyentes. Como
mejoras futuras se podrían considerar:

- Random Search para explorar más valores con el mismo presupuesto;
- búsqueda específica por función y dimensión;
- validación con semillas separadas de las usadas para seleccionar;
- optimización bayesiana si el número de hiperparámetros aumenta;
- intervalos de confianza y pruebas estadísticas entre métodos;
- repetir la validación de los ganadores con más de tres semillas exploratorias.

Estas mejoras no alteran los resultados actuales: documentan cómo hacer más
robusta una selección futura.

## Referencias

Bergstra, J., & Bengio, Y. (2012). *Random Search for Hyper-Parameter
Optimization*. **Journal of Machine Learning Research, 13**, 281–305.
https://jmlr.org/papers/v13/bergstra12a.html
