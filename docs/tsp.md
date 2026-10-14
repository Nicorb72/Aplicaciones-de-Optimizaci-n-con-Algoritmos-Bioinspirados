# TSP de las 47 capitales peninsulares: formulación y algoritmos

Código: `src/tsp/cost_model.py`, `src/tsp/ant_colony.py` y `src/tsp/genetic_tsp.py`. Configuración: `configs/tsp_aco.yaml` y `configs/tsp_ga.yaml`. Este documento describe lo que el código hace, no una versión genérica de los algoritmos.

## 1. El problema

Un vendedor debe visitar las $n = 47$ capitales de provincia de la España peninsular, pasando una sola vez por cada una y volviendo a la ciudad de salida. Un recorrido es una permutación $\pi = (\pi_0, \pi_1, \dots, \pi_{n-1})$ de las ciudades, y su costo es

$$
L(\pi) = \sum_{k=0}^{n-1} C_{\pi_k,\, \pi_{(k+1) \bmod n}}
$$

donde $C_{ij}$ es el costo de ir de la ciudad $i$ a la $j$ (sección 2). Se busca

$$
\pi^{*} = \arg\min_{\pi} L(\pi)
$$

Como el recorrido es cerrado, rotarlo no cambia su costo, así que no importa en qué ciudad empiece. Si los costos fueran simétricos habría $(n-1)!/2 \approx 2.75 \times 10^{57}$ recorridos distintos, por lo que probarlos todos es imposible y se usan metaheurísticas.

## 2. Costo entre dos ciudades

$$
C_{ij} = w \, t_{ij} + p_{ij} + \frac{c}{100} \, d_{ij} \, \varphi, \qquad C_{ii} = 0
$$

| Símbolo    | Significado                   | Unidad   | De dónde sale                                                               |
| ----------- | ----------------------------- | -------- | ---------------------------------------------------------------------------- |
| $w$       | valor de la hora del vendedor | €/h     | `hourly_rate` del YAML (25.0 por defecto); se cambia con `--hourly-rate` |
| $t_{ij}$  | tiempo de viaje por carretera | h        | `times_hours` en `data/tsp/matrices.npz`                                 |
| $p_{ij}$  | peajes del trayecto           | €       | `tolls_eur` en `data/tsp/matrices.npz`                                   |
| $d_{ij}$  | distancia por carretera       | km       | `distances_km` en `data/tsp/matrices.npz`                                |
| $c$       | consumo homologado (WLTP)     | L/100 km | `data/tsp/vehicle_specs.yaml`                                              |
| $\varphi$ | precio del combustible        | €/L     | `data/tsp/vehicle_specs.yaml`                                              |

Las tres matrices están guardadas en el repositorio, así que la ejecución no depende de internet ni de APIs externas. Los valores del vehículo y las fuentes de cada dato, con su fecha de consulta, están en `vehicle_specs.yaml` y en `data/tsp/sources_and_notes.md` (SEAT León 5 puertas 1.5 TSI 130 CV manual; se adopta 5,4 L/100 km, límite inferior del intervalo oficial WLTP 5,4–6,1). El precio es 1,7159 €/L, media nacional PVP con impuestos publicada por MITECO para agosto de 2026. Ambas fuentes se consultaron el 13 de octubre de 2026; páginas, unidades y hashes están en `data/tsp/vehicle_fuel_evidence.json`. El consumo elegido es un supuesto optimista, y el precio mensual es una referencia fija, no una cotización de octubre.

`get_tour_breakdown` descompone el costo de un recorrido en distancia total, tiempo total, costo del tiempo $w\sum t_{ij}$, combustible $\frac{c}{100}\varphi\sum d_{ij}$ y peajes $\sum p_{ij}$.

## 3. Colonia de hormigas (ACO)

**Idea.** Cada hormiga construye un recorrido completo escogiendo la siguiente ciudad al azar, con más probabilidad hacia ciudades baratas (visibilidad) y hacia aristas que otras hormigas usaron en buenos recorridos (feromona). Al terminar cada ciclo la feromona se evapora un poco y las hormigas depositan más en las aristas de sus recorridos, más cuanto mejor haya sido el recorrido.

**Notación.** $\tau_{ij}$ es la feromona de la arista $i \to j$ y $\eta_{ij} = 1/C_{ij}$ la visibilidad ($\eta_{ij}=0$ si $C_{ij}=0$). $\mathcal{N}_i^k$ son las ciudades que la hormiga $k$ aún no ha visitado estando en $i$, y $L_k = L(\pi^{(k)})$ es el costo (en euros) de su recorrido. $m$ es el número de hormigas.

**Feromona inicial**, uniforme:

$$
\tau_{ij}(0) = \tau_0 = \frac{1}{n \, \bar{C}}
$$

con $\bar{C}$ la media de los costos positivos de la matriz.

**Regla de transición.** Estando en $i$, la hormiga $k$ elige $j \in \mathcal{N}_i^k$ con probabilidad

$$
P_{ij}^{k} = \frac{\tau_{ij}^{\alpha} \, \eta_{ij}^{\beta}}{\sum_{l \in \mathcal{N}_i^{k}} \tau_{il}^{\alpha} \, \eta_{il}^{\beta}}
$$

Si todos los pesos fueran cero o no finitos, elige uniformemente entre las ciudades restantes.

**Actualización de la feromona** al final de cada iteración:

$$
\tau_{ij} \leftarrow (1-\rho)\,\tau_{ij} + \sum_{k=1}^{m} \Delta\tau_{ij}^{k} + \Delta\tau_{ij}^{\text{élite}}
$$

$$
\Delta\tau_{ij}^{k} = \begin{cases} Q / L_k & \text{si la arista } \{i,j\} \text{ está en el recorrido de la hormiga } k \\ 0 & \text{en otro caso} \end{cases}
$$

$$
\Delta\tau_{ij}^{\text{élite}} = \begin{cases} 2Q / L_{\text{mejor}} & \text{si la arista } \{i,j\} \text{ está en el mejor recorrido hallado hasta ahora} \\ 0 & \text{en otro caso} \end{cases}
$$

**Algoritmo.**

1. Inicializar $\tau_{ij} = \tau_0$.
2. Repetir `iterations` veces:
   1. Cada una de las $m$ hormigas parte de una ciudad al azar y construye un recorrido con la regla de transición.
   2. Calcular $L_k$ de cada recorrido y actualizar el mejor recorrido global.
   3. Evaporar: multiplicar toda la feromona por $(1-\rho)$.
   4. Depositar $Q/L_k$ en las aristas de cada hormiga y $2Q/L_{\text{mejor}}$ en las del mejor global.
3. Devolver el mejor recorrido y su costo.

**Parámetros** (`configs/tsp_aco.yaml`):

| Parámetro     | Símbolo   | Valor |
| -------------- | ---------- | ----- |
| `n_ants`     | $m$      | 25    |
| `iterations` |            | 80    |
| `alpha`      | $\alpha$ | 1.0   |
| `beta`       | $\beta$  | 2.5   |
| `rho`        | $\rho$   | 0.25  |
| `q`          | $Q$      | 100.0 |
| `seed`       |            | 42    |

**Detalles de implementación.**

- Depositan **todas** las hormigas de la iteración, no solo la mejor, y además el mejor global recibe un refuerzo elitista con peso fijo 2 (no es un parámetro).
- No hay límites inferior ni superior para la feromona.
- El depósito se hace en ambos sentidos ($\tau_{uv}$ y $\tau_{vu}$), lo que supone costos aproximadamente simétricos.
- Evaluaciones del costo de un recorrido: $m \times \text{iterations} = 25 \times 80 = 2000$.

## 4. Algoritmo genético (GA)

**Idea.** Se mantiene una población de recorridos. En cada generación los mejores pasan intactos, y el resto se reemplaza por hijos obtenidos cruzando padres elegidos por torneo y mutándolos de vez en cuando.

**Representación.** Cada individuo es una permutación de las $n$ ciudades; su aptitud es el costo $L(\pi)$, que se minimiza. La población inicial son `population_size` permutaciones aleatorias.

**Selección por torneo.** Se eligen al azar `tournament_size` individuos distintos y gana el de menor costo. Se hacen dos torneos independientes para obtener los padres $p_1$ y $p_2$ (pueden coincidir).

**Cruce de orden (variante de OX).** Se sortean dos puntos de corte $a < b$. El hijo copia de $p_1$ el tramo $[a, b]$ en las mismas posiciones, y las posiciones libres se rellenan de izquierda a derecha con las ciudades de $p_2$, en el orden en que aparecen en $p_2$, saltando las ya copiadas. Siempre se aplica (no hay probabilidad de cruce) y el resultado es siempre una permutación válida. Ejemplo con $p_1 = (0,1,\dots,9)$, $p_2 = (9,8,\dots,0)$ y corte en las posiciones 3 a 5:

$$
\text{hijo} = (9, 8, 7, \underline{3, 4, 5}, 6, 2, 1, 0)
$$

El OX clásico rellena empezando después del segundo corte; esta versión rellena desde la posición 0.

**Mutación por inversión.** Con probabilidad $\mu$ (`mutation_rate`) se sortean dos posiciones $i < j$ y se invierte el tramo entre ellas:

$$
(\pi_i, \pi_{i+1}, \dots, \pi_j) \leftarrow (\pi_j, \dots, \pi_{i+1}, \pi_i)
$$

Es un movimiento tipo 2-opt. Solo se aplica a los hijos, no a la élite.

**Algoritmo.**

1. Generar la población inicial y calcular el costo de cada individuo.
2. Repetir `generations` veces:
   1. Copiar a la nueva población los `elite_size` mejores individuos, sin cambios.
   2. Mientras la nueva población no esté completa: elegir $p_1$ y $p_2$ por torneo, cruzarlos con OX y mutar el hijo con probabilidad $\mu$.
   3. Reemplazar la población y recalcular los costos.
   4. Actualizar el mejor recorrido global.
3. Devolver el mejor recorrido y su costo.

**Parámetros** (`configs/tsp_ga.yaml`):

| Parámetro                | Valor |
| ------------------------- | ----- |
| `population_size`       | 100   |
| `generations`           | 250   |
| `mutation_rate` $\mu$ | 0.5   |
| `tournament_size`       | 6     |
| `elite_size`            | 2     |
| `seed`                  | 42    |

**Evaluaciones del costo.** En cada generación se recalcula el costo de toda la población, incluida la élite, así que son $\text{population\_size} \times (\text{generations} + 1) = 100 \times 251 = 25\,100$.

## 5. Para comparar ACO y GA

Con las configuraciones actuales ACO evalúa 2000 recorridos y GA 25 100, unas 12.5 veces más. Para comparar los dos algoritmos de forma justa conviene igualar el presupuesto de evaluaciones, como se hace en la Parte 1, y repetir con varias semillas.

Ambos usan `numpy.random.default_rng(seed)`, así que una corrida con la misma semilla y la misma configuración da el mismo resultado.

## 6. Cómo ejecutarlo

Desde la raíz del repositorio y con el entorno activado:

```
python -m experiments.run_tsp --config configs/tsp_aco.yaml
python -m experiments.run_tsp --config configs/tsp_ga.yaml
python -m experiments.run_tsp --config configs/tsp_aco.yaml --hourly-rate 50.0
python -m experiments.run_tsp --config configs/tsp_aco.yaml --study-hourly-rates
```

Los resultados se guardan en `results/tsp/aco/` y `results/tsp/ga/`.

## 7. Escenarios de peajes provisionales

El comando `python -m experiments.run_toll_study` ejecuta 18 corridas: ACO y GA,
factores de peaje 0, 1 y 2, y semillas 42, 43 y 44. La tarifa del vendedor es
25 €/h por defecto. Solo cambia el componente de peajes:

$$ C_{ij}(s)=w t_{ij}+s p_{ij}+\frac{c}{100}d_{ij}\varphi. $$

Se guardan las corridas, configuraciones, hashes de los datos, media, desviación
muestral y mejor costo. Para cada semilla, la ruta obtenida con factor 1 se
revalúa sin cambiar su orden en los tres escenarios. Así se distingue el efecto
directo de cambiar un precio de la variabilidad de volver a ejecutar el método.
Los cambios de ruta se comparan mediante aristas dirigidas, porque las matrices
viales no son simétricas. Se conservan los distintos presupuestos de ACO y GA;
el estudio no demuestra superioridad de un algoritmo.

El resultado se publica con `python -m scripts.build_blog --tsp-only`, en la
Tabla 4 del blog y `docs/datos/sensibilidad_peajes.json`. Los mapas y resultados
principales siguen representando factor 1 y semilla 42.

**Limitaciones:** el factor 0 significa excluir el componente monetario de
peajes, no buscar carreteras gratuitas. El factor 2 duplica importes registrados,
pero no completa los desconocidos ni es una cota superior real. Los ceros sin
verificar siguen siendo cero. Se trata de escenarios hipotéticos y no de
tarifas oficiales verificadas; tres semillas solo aportan evidencia exploratoria.
