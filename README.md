# optimization-project

Proyecto base para experimentos de optimización con funciones benchmark
(Rosenbrock y Rastrigin) y algoritmos bioinspirados.

## Instalación del entorno

Entorno probado: Linux y Python **3.11.16**. Las versiones de las dependencias
directas e indirectas están fijadas con `==` en `requirements.txt`.
`.python-version` indica a `uv` qué versión de Python utilizar.

Desde la raíz del repositorio, con `uv` instalado, crea el entorno una vez:

```bash
uv venv
uv pip sync requirements.txt
```

La instalación requiere acceso a internet si Python o los paquetes no están
disponibles en la caché local. Los experimentos posteriores funcionan sin conexión.
`uv pip sync` instala las versiones del archivo y retira del entorno los paquetes
que no figuren en él. `.venv/` está excluido de Git; cada integrante crea el suyo.

Activa el entorno en cada terminal nueva:

```bash
source .venv/bin/activate
```

Para comprobarlo:

```bash
python --version
MPLBACKEND=Agg python -m pytest -q
```

## Parte 1 completa: un comando

Con el entorno activado, desde la raíz del repositorio:

```bash
MPLBACKEND=Agg python -m experiments.run_part1
```

Ejecuta **300 corridas**: GD sobre Rosenbrock y Rastrigin en 2D y 3D, y PSO,
evolutivo y DE sobre ambas funciones en 2D; 30 corridas por configuración.
Los parámetros están en `configs/part1.yaml`, incluidas las semillas 42–71,
el umbral de éxito, los tamaños de población y los coeficientes de los algoritmos.

Genera en `results/part1/`:

- `raw/{función}/{método}/{dimensión}/`: CSV de corridas, JSON con configuración,
  estadísticas y costos; trayectorias NPZ y, para PSO, posiciones del enjambre.
- `figures/`: convergencia y trayectoria por configuración.
- `animations/`: GIF de GD 2D/3D y PSO 2D para ambas funciones.
- `comparisons/all/report.md`: tablas y discusión de resultados y costos.
- `comparisons/all/report.html`: informe visual offline, con tablas, gráficas y GIF integrados.
- `comparisons/all/comparison.csv`, `comparison.json` y `environment.json`:
  datos de la comparación y versiones utilizadas.

El costo equivalente es `N_f + 2*d*N_grad`: una convención basada en diferencias
centrales, aunque GD usa derivadas analíticas. Los experimentos principales 2D
usan 40001 unidades para GD completado y 40000 para cada heurístico. Se informan
también los contadores por separado. Los resultados 3D de GD se analizan aparte.

Consulta la [metodología y guía de sustentación](docs/parte1_metodologia.md) y la
[copia de los resultados verificados](docs/resultados/report.md). El reporte no
afirma superioridad universal de un método ni confunde el costo equivalente con
el tiempo de ejecución.
La [verificación de esta entrega](docs/verificacion_parte1.md) registra las pruebas
y la demostración, junto con los límites de lo que se ha comprobado.

### Demostración corta

```bash
MPLBACKEND=Agg python -m experiments.run_part1 --config configs/part1_demo.yaml
```

Mantiene 30 corridas por configuración, con un presupuesto de búsqueda menor y
GIF de 48 fotogramas a 4 fps (12 segundos), con ritmo por movimiento. Escribe en `results/part1_demo/`, sin reemplazar los
resultados principales. El experimento completo puede tardar varios minutos;
la demostración es la que se debe cronometrar en la máquina de sustentación.

### Mostrar el informe en pantalla

Abre `results/part1/comparisons/all/report.html` con el navegador para presentar
los resultados principales. La demo tiene su propio informe en
`results/part1_demo/comparisons/all/report.html` y se identifica como demostración.
Los informes se generan automáticamente con el comando de experimentos.

En Linux, desde la raíz del repositorio:

```bash
xdg-open results/part1/comparisons/all/report.html
```

La página funciona sin conexión y muestra imágenes y GIF sin instalar nada.
Conserva la carpeta de resultados completa: las imágenes son archivos enlazados.
Para imprimir o guardar un PDF usa Ctrl+P; en el PDF los GIF serán estáticos.
Para ver el Markdown dentro de VS Code, abre `report.md` y pulsa Ctrl+Shift+V.

Antes de entregar, revisa [uso de IA y verificaciones](docs/uso_ia_y_verificaciones.md)
y los [pendientes de entrega](docs/verificacion_parte1.md#entregables-externos).
Repositorio: https://github.com/Nicorb72/Aplicaciones-de-Optimizaci-n-con-Algoritmos-Bioinspirados

### Selección y regeneración

```bash
# Ejecutar solamente un método sobre las dos funciones:
MPLBACKEND=Agg python -m experiments.run_pso
MPLBACKEND=Agg python -m experiments.run_evolutionary
MPLBACKEND=Agg python -m experiments.run_differential_evolution

# Elegir una función, método y dimensión:
MPLBACKEND=Agg python -m experiments.run_part1 --function rastrigin --method gd --dimension 3

# Rehacer las figuras y GIF, sin volver a optimizar:
MPLBACKEND=Agg python -m experiments.run_part1 --render-only

# Ejecutar solo cálculos y tablas, o cambiar el destino/fotogramas:
MPLBACKEND=Agg python -m experiments.run_part1 --no-visuals
MPLBACKEND=Agg python -m experiments.run_part1 --output-dir /tmp/parte1 --frames 60
```

`--render-only` exige resultados guardados con la misma configuración.
Cada selección escribe su comparación en un subdirectorio propio para no
sobrescribir la tabla completa. Las rutas de salida relativas se resuelven desde
la raíz del repositorio. Repetir una configuración reemplaza sus archivos de salida.
`--frames` controla los fotogramas, no las iteraciones ni los puntos guardados.
Con `pacing: movement` (predeterminado en ambos YAML), el 90% del tiempo visual
se reparte según la distancia y el 10% según las iteraciones. Se interpolan
posiciones entre estados consecutivos para mostrar los desplazamientos grandes
con más calma; el GIF lo indica y muestra la iteración aproximada con `≈`.
El valor de f en ese punto intermedio es solo visual, no un resultado nuevo.
En PSO, el ritmo usa el movimiento de todas las partículas, no solo del mejor.
Con `--pacing iterations` se recupera la selección original de iteraciones reales.

Para regenerar la demo con el nuevo ritmo, sin recalcular las corridas:

```bash
MPLBACKEND=Agg python -m experiments.run_part1 --config configs/part1_demo.yaml --render-only
```

Para una reproducción más fluida de la misma duración, puedes agregar
`--frames 120 --fps 10`; requiere más tiempo de renderizado. Recarga el informe
con Ctrl+Shift+R para evitar que el navegador conserve los GIF anteriores.
En PSO, la línea representa los mejores puntos conocidos y los puntos lavanda
representan las partículas reales. La corrida ilustrada es la primera exitosa,
o la primera completada con valor finito cuando no hay éxitos.

El comando independiente de Rastrigin también quedó reparado:

```bash
MPLBACKEND=Agg python -m experiments.run_rastrigin_gd
```

Usa `configs/rastrigin.yaml`: 30 corridas por dimensión, estadísticas, gráficas y
GIF. Sus archivos van a `results/raw/rastrigin_gd`, `results/figures/rastrigin_gd`
y `results/animations/rastrigin_gd`.

## Persona 1: Rosenbrock + descenso por gradiente

Desde la raíz del repositorio y con las dependencias instaladas en el entorno
Python activo, ejecuta:

```bash
MPLBACKEND=Agg PYTHONPATH=src python -m experiments.run_persona1
```

El comando ejecuta 30 corridas en 2D y 30 en 3D, guarda sus estadísticas y
trayectorias, genera las gráficas de ambas dimensiones y crea los GIF 2D y 3D.
`MPLBACKEND=Agg` permite generar los archivos sin abrir ventanas.

- `configs/rosenbrock.yaml`: parámetros de las corridas 2D.
- `configs/rosenbrock_3d.yaml`: parámetros de las corridas 3D.
- Cada configuración usa las semillas `42` a `71` (`seed + índice de corrida`).
- Resultados: `results/raw/rosenbrock_gd/{2d,3d}/`.
- Gráficas: `results/figures/rosenbrock_gd/{2d,3d}/`.
- GIF 2D: `results/animations/rosenbrock_gd/2d/trajectory_run_001.gif`.
- GIF 3D: `results/animations/rosenbrock_gd/3d/trajectory_run_001.gif`.

Puedes usar otros archivos con `--config-2d` y `--config-3d`, y cambiar la
animación con `--frames`, `--fps` y `--run-id`. Estas opciones se aplican a ambos
GIF. La corrida elegida debe haber terminado con un valor finito en ambas
dimensiones; no necesita alcanzar el umbral de éxito.
Las gráficas seleccionan automáticamente la primera corrida exitosa o, si no
hay éxitos, la primera completada con valor finito.

Las rutas relativas de `output_dir` en los YAML se resuelven desde la raíz del
repositorio. `--figures-dir` y `--animations-dir` permiten cambiar los destinos
visuales; si son relativos, se resuelven desde el directorio de ejecución.
Al repetir el comando se sobrescriben los archivos de salida con el mismo nombre.
Consulta todas las opciones con `python -m experiments.run_persona1 --help`
usando el mismo entorno y `PYTHONPATH=src`.

### Qué representa el GIF 3D

Los ejes son las tres variables de entrada `x1`, `x2`, `x3`; la estrella indica
el mínimo global `(1, 1, 1)`. El corazón recorre los puntos guardados por GD y la
tarjeta muestra `f(x1, x2, x3)`. El tercer eje **no** es el valor de la función.
La cámara y los límites permanecen fijos para facilitar la lectura del movimiento.
Las superficies transparentes rosa y lavanda representan **f=1 y f=10**,
respectivamente: ilustran el valle de la función de tres variables. Se calculan
despejando x3 en la ecuación f(x1,x2,x3)=c; no son una superficie de Rosenbrock 2D.

Para regenerar solo el GIF 3D desde los resultados guardados:

```bash
MPLBACKEND=Agg PYTHONPATH=src python -m visualization.animations --results-dir results/raw/rosenbrock_gd/3d
```

La visualización no vuelve a ejecutar GD. Sus evaluaciones de Rosenbrock sirven
para dibujar y no se suman a los contadores del experimento.

## Parte 2: Optimización combinatoria (TSP - 47 Capitales de España Peninsular)

Optimización de la ruta cerrada del vendedor viajero que recorre las 47 capitales de provincia de la España peninsular (excluyendo islas, Ceuta y Melilla) mediante **Colonias de Hormigas (ACO)** y **Algoritmos Genéticos (GA)**.

### Datos y reproducibilidad offline
- Capitales y coordenadas: `data/tsp/spain_capitals.csv` (47 ciudades peninsulares con latitud y longitud).
- Matrices guardadas (distancias por carretera, tiempos y peajes): `data/tsp/matrices.npz`.
- Vehículo y precios: `data/tsp/vehicle_specs.yaml` (SEAT León 1.5 TSI 130 CV, consumo 5.4 L/100km WLTP, Gasolina 95 a 1.58 €/L con fuente MITECO).
- Justificación de datos y estado de autopistas de peaje: `data/tsp/sources_and_notes.md`.

### Ejecución con un solo comando

Para ejecutar **Colonias de Hormigas (ACO)**:
```bash
python -m experiments.run_tsp --config configs/tsp_aco.yaml
```

Para ejecutar **Algoritmos Genéticos (GA)**:
```bash
python -m experiments.run_tsp --config configs/tsp_ga.yaml
```

Para evaluar el impacto de la tarifa horaria del vendedor (`--hourly-rate`) o ejecutar el estudio paramétrico (`--study-hourly-rates`):
```bash
python -m experiments.run_tsp --config configs/tsp_aco.yaml --hourly-rate 50.0
python -m experiments.run_tsp --config configs/tsp_aco.yaml --study-hourly-rates
```

- Salidas generadas:
  - Mapa del recorrido estático: `results/tsp/{aco,ga}/spain_optimal_tour.png`.
  - Animación GIF de la evolución: `results/tsp/{aco,ga}/tour_evolution.gif`.
  - Resumen numérico y desglose de costos: `results/tsp/{aco,ga}/tsp_summary.json`.
