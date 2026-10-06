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
