# Parte 1: metodología y guía para la sustentación

## Qué se compara

Se estudian Rosenbrock y Rastrigin. GD se ejecuta en 2D y 3D; los cuatro métodos
se comparan en 2D. Son diez configuraciones, con 30 corridas cada una: 300 corridas.
El archivo `configs/part1.yaml` conserva todos los parámetros. Las semillas son
42 a 71. Cada corrida construye su propio generador `default_rng(seed)`.
Reutilizar esos identificadores entre métodos facilita repetir el experimento;
no significa que una población y un punto inicial sean condiciones idénticas.

El comando principal es `MPLBACKEND=Agg python -m experiments.run_part1`.
El informe numérico generado está en `results/part1/comparisons/all/report.md`.
La copia versionada de los resultados comprobados está en [resultados/report.md](resultados/report.md).
Todas las figuras de ese informe tienen título, fuente y una referencia en el texto.

## Funciones, dominio y mínimo global

Rosenbrock, para d=2 o d=3:

\[
f(x)=\sum_{i=1}^{d-1}\left[100(x_{i+1}-x_i^2)^2+(1-x_i)^2\right].
\]

Cada sumando es no negativo. En x=(1,…,1), todos se anulan: el mínimo global es
f=0. En 2D los dos términos obligan a x1=x2=1; en 3D sucede lo mismo con x3.
El intervalo inicial elegido para este experimento es [-2,2] en cada coordenada,
que contiene el mínimo; es una elección del proyecto, no el único dominio posible.
La forma de valle curvo y estrecho dificulta el avance hacia el mínimo
([Simon Fraser University, s. f.-b](https://www.sfu.ca/~ssurjano/rosen.html)).

Su gradiente se obtiene acumulando dos contribuciones por cada par consecutivo:

\[
g_i\mathrel{+}= -400x_i(x_{i+1}-x_i^2)+2(x_i-1),\qquad
g_{i+1}\mathrel{+}=200(x_{i+1}-x_i^2).
\]

Esto explica las dos asignaciones vectorizadas de `rosenbrock_gradient`: una
coordenada interior participa en dos términos de la suma.

Rastrigin:

\[
f(x)=10d+\sum_{i=1}^d[x_i^2-10\cos(2\pi x_i)],\qquad
g_i=2x_i+20\pi\sin(2\pi x_i).
\]

Su mínimo global es f(0,…,0)=0: cada término puede escribirse como
x_i²+10[1−cos(2πx_i)], que es no negativo. Usamos el intervalo [-5.12,5.12]
en cada coordenada. La oscilación introduce muchos mínimos locales
([Simon Fraser University, s. f.-a](https://www.sfu.ca/~ssurjano/rastr.html)).

Las funciones están definidas matemáticamente en R^d. Los intervalos anteriores
se usan para inicializar los algoritmos; los heurísticos también recortan sus
propuestas a ellos. GD no tiene proyección. Esta diferencia se declara como una
limitación de la comparación; no se afirma que los cuatro algoritmos impongan
exactamente las mismas restricciones.

## Algoritmos implementados

**GD.** Actualiza x^(t+1)=x^t−α∇f(x^t), con α=0.001 y 10000 iteraciones.
Calcula el gradiente analítico una vez por intento y f una sola vez al final.
Guarda el punto inicial y cada punto aceptado. Si el gradiente, el candidato o
el valor final dejan de ser finitos, registra `diverged`. `completed` significa
que terminó el presupuesto; el éxito se evalúa aparte mediante f≤0.0001.
El campo histórico `best_value` de GD contiene el valor FINAL, no un mínimo
buscado a lo largo de toda la trayectoria. Las tablas lo identifican como tal.

**PSO.** Para cada partícula se mantienen posición x, velocidad v, mejor posición
individual p y mejor posición colectiva g. Se actualiza:

\[
v\leftarrow wv+c_1r_1(p-x)+c_2r_2(g-x),\quad
x\leftarrow\operatorname{clip}(x+v,l,u).
\]

Los vectores r1 y r2 tienen componentes uniformes independientes en [0,1).
Usamos w=0.7 y c1=c2=1.4. Las velocidades iniciales son cero. Se evalúan las
40 posiciones iniciales y 40 posiciones en cada una de las 999 iteraciones.
Se conservan el mejor valor ya calculado y el historial completo del enjambre;
no se vuelve a evaluar g al retornar. La descripción conceptual del enjambre
puede consultarse en [IEEE Technology Navigator](https://technav.ieee.org/topic/particle-swarm-optimization/).

**Evolutivo.** La mejor mitad de la población es la élite. Se eligen dos padres
de esa élite con reemplazo. Un hijo antes de mutar es
z=λp1+(1−λ)p2, con λ uniforme en [0,1). Después se suma ruido gaussiano
independiente de desviación σ=0.1 por coordenada y se recorta al intervalo.
La nueva población combina élite e hijos. Se reutilizan los valores de la élite:
40 evaluaciones iniciales y 20 por cada una de las 1998 generaciones.
Es una variante sencilla de codificación real, descrita aquí tal como se
implementó; no se presenta como reproducción exacta de un algoritmo publicado.

**DE.** Se eligen tres individuos distintos a, b y c, excluyendo al individuo
objetivo. El donante es v=clip(a+F(b−c),l,u), con F=0.8. Cada componente del
candidato toma el donante con probabilidad CR=0.7; si ninguna fue elegida, se
fuerza una componente aleatoria. Se acepta el candidato si mejora al objetivo.
Las sustituciones son inmediatas: pueden influir en las propuestas posteriores
de la misma generación. Es la variante concreta usada aquí, basada en el
principio de evolución diferencial de [Storn y Price (1997)](https://doi.org/10.1023/A:1008202821328).
Hace 40 evaluaciones iniciales y 40 en cada una de las 999 generaciones.

## Qué significa comparar costos

Se guardan N_f y N_grad separados en cada fila de `runs.csv`. Definimos:

\[
C=N_f+2dN_{\nabla f}.
\]

La motivación son las diferencias centrales:

\[
\frac{\partial f}{\partial x_i}\approx
\frac{f(x+he_i)-f(x-he_i)}{2h}.
\]

Hay dos llamadas a f por coordenada: 2d para el vector completo. Esta es la
convención sugerida en el enunciado. **El código usa gradientes analíticos**:
no ejecuta esas 2d llamadas. Por eso C es un costo equivalente para comparar,
no tiempo real ni una medición del costo interno de la derivada.

En 2D, GD completado cuesta 1+4·10000=40001. Los tres heurísticos cuestan
40000 llamadas reales a f y cero al gradiente. La diferencia es una unidad.
GD 3D completado cuesta 60001 y se analiza aparte. Si GD diverge antes, se
incluyen sus intentos efectivamente ejecutados en el conteo; el menor costo
no compensa que haya fracasado. Las llamadas de las visualizaciones no forman
parte del optimizador y no alteran sus contadores.

## Estadísticas y selección visual

La tasa de éxito usa todas las corridas. Media, desviación muestral, mejor y
peor consideran solo finales completados y finitos. Cada tabla informa cuántos
se excluyeron. Con cero finales válidos se usa N/D; con uno, la desviación es N/D.
Los costos medios incluyen todas las corridas, incluidas las divergentes.

La animación elige la primera corrida exitosa o, si no hay éxitos, la primera
completada. No pretende representar la mediana de las 30 corridas. La estrella
es el óptimo conocido, usado solo para dibujar, no para dirigir el optimizador.
En PSO se muestran las partículas reales y el mejor punto conocido; la línea
de mejores puntos puede saltar de una partícula a otra.

## Cómo se ilustra Rosenbrock 3D

Los tres ejes son x1, x2 y x3. Para mostrar la función se dibujan superficies
de nivel f=1 y f=10, dentro de los límites visibles. Partimos de:

\[
A=100(x_2-x_1^2)^2+(1-x_1)^2+(1-x_2)^2,\qquad
f=A+100(x_3-x_2^2)^2.
\]

Al imponer f=c se obtiene:

\[
x_3=x_2^2\pm\sqrt{(c-A)/100},\qquad A\le c.
\]

`rosenbrock_isosurface` calcula esas dos ramas. Donde A>c no hay solución real,
por eso se usa NaN para no dibujar. Las superficies transparentes son una malla
de esas ramas, no una superficie z=f(x1,x2) de una función de dos variables.
El panel lateral muestra el valor de f sobre el punto que se mueve.
Las pruebas sustituyen puntos de las ramas en Rosenbrock y verifican f=c.

## Mapa del código nuevo

| Archivo | Responsabilidad y lectura del código |
|---|---|
| `experiments/run_part1.py` | `configurations` combina función, método y dimensión; `main` lee opciones, ejecuta o carga resultados, dibuja y genera el informe. |
| `optimization/benchmark.py` | Selecciona la función y el optimizador; crea una semilla por corrida; calcula estadísticas y costos medios. |
| `optimization/population_utils.py` | Valida límites/tamaños y convierte los historiales al formato común. |
| `optimization/result_storage.py` | Guarda CSV, configuración/resumen y arrays numéricos NPZ, sin volver a optimizar. |
| `optimization/comparison.py` | Construye tablas y párrafos desde los resultados reales; conserva las versiones ejecutadas. |
| `visualization/plot_benchmark.py` | Lee archivos guardados, selecciona explícitamente una corrida y genera las dos gráficas por configuración. |
| `visualization/animations.py` | `animate_saved` comparte el diseño 2D/3D y GD/PSO; `set_data_3d` actualiza tres coordenadas; el enjambre usa `population_history`. |
| `tests/test_part1.py` | Cuenta llamadas reales, verifica semillas, costos, superficies, cobertura y ejecución del comando. |

Los módulos de `optimization/` están dentro de `src/`. Para inspeccionar una
corrida, abre primero su `summary.json`, luego la fila correspondiente de
`runs.csv` y finalmente su array `run_XXX` en `trajectories.npz`.

## Reproducibilidad y límites de la entrega

`configs/part1_demo.yaml` mantiene 30 corridas y reduce el presupuesto; sus
resultados van a `results/part1_demo`, separados de los principales. La
demostración sirve para mostrar el flujo, no para sustituir el estudio principal.
`--render-only` evita recalcular los experimentos y verifica que la configuración
guardada coincida. Las figuras se pueden regenerar sin conexión a internet.

El código, el informe y la bibliografía no equivalen a publicar el blog ni a
grabar el video individual. Esos entregables y la prueba en otra máquina deben
realizarlos los integrantes. La ejecución en una copia limpia de esta máquina
no se presenta como prueba en otra máquina.

## Referencias

IEEE. (s. f.). *Particle swarm optimization*. IEEE Technology Navigator.
https://technav.ieee.org/topic/particle-swarm-optimization/

Simon Fraser University. (s. f.-a). *Rastrigin function*. Virtual Library of Simulation Experiments: Test Functions and Datasets.
https://www.sfu.ca/~ssurjano/rastr.html

Simon Fraser University. (s. f.-b). *Rosenbrock function*. Virtual Library of Simulation Experiments: Test Functions and Datasets.
https://www.sfu.ca/~ssurjano/rosen.html

Storn, R., & Price, K. (1997). Differential evolution—A simple and efficient heuristic for global optimization over continuous spaces.
*Journal of Global Optimization, 11*, 341–359. https://doi.org/10.1023/A:1008202821328

Fuentes web consultadas el 7 de octubre de 2026. Las fórmulas de gradiente y
las isosuperficies se derivaron explícitamente de las funciones implementadas.
