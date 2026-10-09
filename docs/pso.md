# PSO 

Autor: Sebastián Cataño 

Implementación: `src/optimization/pso.py` (función `run_pso`). Se ejecuta con `experiments/run_pso.py`, que llama a `run_part1.main` con el método `pso`.

## Qué hace

PSO busca el mínimo de una función imitando a una bandada de pájaros que busca comida en un terreno que no puede ver completo. Cada pájaro es una **partícula**: un punto del espacio de búsqueda (en 2D, un par `(x1, x2)`). El conjunto de partículas es el **enjambre**. Cada partícula solo sabe cuánto vale la función donde está parada, pero se mueve usando tres influencias: la dirección que ya llevaba, el mejor sitio que ella ha visitado y el mejor sitio que ha encontrado cualquiera del enjambre. Ninguna partícula es lista por sí sola; el enjambre explora bien en conjunto. PSO no usa el gradiente de la función.

## Qué guarda cada partícula

- `x`: su posición actual en el espacio de búsqueda.
- `v`: su velocidad, es decir, cuánto y hacia dónde se desplaza en el siguiente paso. En esta implementación empieza en cero.
- `p_best`: la mejor posición (menor valor de f) que esa partícula ha visitado.
- `g_best`: la mejor posición que ha encontrado cualquier partícula del enjambre. Es una sola y se comparte.

Las posiciones iniciales se sortean de forma uniforme dentro del dominio, con una semilla fija para que los resultados sean reproducibles.

## Actualización de cada partícula

```
v = inertia·v + cognitive·r1·(p_best − x) + social·r2·(g_best − x)
x = x + v
```

- `inertia`: cuánta de la velocidad anterior se conserva. Un valor alto hace que la partícula explore más y un valor bajo la frena y le permite afinar.
- `cognitive`: fuerza del jalón hacia el mejor sitio personal (`p_best`), es decir, la "memoria" de la partícula.
- `social`: fuerza del jalón hacia el mejor sitio del enjambre (`g_best`), es decir, la influencia del grupo.
- `r1`, `r2`: números aleatorios entre 0 y 1, nuevos en cada paso y en cada coordenada. Evitan que todas las partículas se muevan igual y le dan al algoritmo su carácter estocástico.

Ejemplo en 1D: con `x = 2`, `v = 1`, `p_best = 3`, `g_best = 5`, `inertia = 0.7`, `cognitive = social = 1.5`, `r1 = 0.5` y `r2 = 0.2`, la nueva velocidad es 0.7 + 0.75 + 0.9 = 2.35 y la nueva posición es 4.35.

## Algoritmo

1. Sortear las posiciones iniciales dentro del dominio y evaluar f en cada partícula.
2. Anotar `p_best` de cada partícula (al inicio, su posición) y `g_best` (la mejor de todas).
3. Repetir durante `iterations` pasos:
   1. Actualizar velocidades y posiciones con la fórmula anterior.
   2. Recortar las posiciones al dominio.
   3. Evaluar f en las nuevas posiciones.
   4. Si una partícula mejoró, actualizar su `p_best`.
   5. Actualizar `g_best` con la mejor de todas.
4. Devolver el mejor punto encontrado y su valor.

## Parámetros en `configs/part1.yaml`

| Parámetro | Valor |
|---|---|
| `particles` | 40 |
| `iterations` | 999 |
| `inertia` | 0.7 |
| `cognitive` | 1.4 |
| `social` | 1.4 |

Los valores se cambian en el archivo de configuración, sin tocar el código.

## Por qué `iterations` es 999 y no 1000

Para comparar los métodos de forma justa, todos gastan el mismo presupuesto de evaluaciones de f. En PSO:

```
evaluaciones de f = particles + iterations · particles
                  = 40 + 999 · 40
                  = 40000
```

Las 40 evaluaciones iniciales también cuentan, por eso con 1000 iteraciones el total sería 40040. El descenso por gradiente en 2D cuesta 1 + 2·2·10000 = 40001 unidades equivalentes, y los otros dos métodos heurísticos están ajustados a 40000. PSO no calcula gradientes, así que sus evaluaciones de gradiente son 0, y eso se reporta por separado.

## Qué pasa en la frontera del dominio

Después de calcular `x + v`, el código aplica `np.clip(x + v, low, high)`: cada coordenada que se sale del dominio se recorta al borde, así que la partícula nunca evalúa f fuera de los límites. La velocidad no se modifica. Esto significa que una partícula pegada al borde puede seguir "empujando" hacia afuera mientras los jalones de `p_best` y `g_best` no la devuelvan. Es una decisión de diseño habitual y sencilla; otras variantes anulan la velocidad al chocar con el borde o la hacen rebotar.

## Qué guarda para las animaciones

Además del mejor valor de cada iteración, `run_pso` devuelve `population_history`: las posiciones de todas las partículas en cada iteración. Con esa información se dibuja el GIF del enjambre en 2D.

## Cómo ejecutarlo

Desde la raíz del repositorio y con el entorno activado:

```
python -m experiments.run_pso --config configs/part1_demo.yaml
```

La demo usa un presupuesto menor que el experimento principal, y sus resultados se guardan en `results/part1_demo/`.