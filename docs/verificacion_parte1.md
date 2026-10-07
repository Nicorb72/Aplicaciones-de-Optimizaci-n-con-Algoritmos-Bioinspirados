# Verificación de la Parte 1

Fecha: 7 de octubre de 2026. Python 3.11.16, dependencias de `requirements.txt`,
backend gráfico Agg. Comprobaciones realizadas sobre los cambios de esta entrega.

| Comprobación | Resultado observado |
|---|---|
| Experimento principal, `configs/part1.yaml` | 10 configuraciones, 30 corridas cada una: 300 corridas. |
| Resultados persistidos | CSV por corrida, resumen/configuración JSON y trayectorias NPZ. |
| Historiales heurísticos | Valores, evaluaciones y, en PSO, posiciones del enjambre guardados. |
| Visualizaciones principales | 20 PNG y 6 GIF de 30 fotogramas, 1000×650 píxeles. |
| GIF 3D de Rosenbrock | Superficies f=1 y f=10 junto a la trayectoria; sustitución numérica f=c verificada. |
| Rastrigin independiente | Comando probado en 2D/3D, 30 corridas cortas por dimensión, gráficas y GIF en directorios temporales. |
| Contadores | Contrastados con un objetivo instrumentado que cuenta llamadas reales en los tres heurísticos. |
| Semillas | Corridas 42–71, sin reutilizar el estado del generador entre corridas. |
| Suite de pruebas | 84 pruebas aprobadas en el entorno del proyecto. |
| Copia limpia del código y entorno reconstruido | 84 pruebas aprobadas; instalación offline desde caché con las 16 versiones fijadas. |
| Demostración completa | 31,32 segundos en esta máquina; exit code 0. |

La copia limpia incluyó los archivos versionados y los nuevos archivos de estos
cambios, sin los resultados previos ni el entorno original. No es una prueba
en otra máquina; esa comprobación del enunciado sigue correspondiendo al equipo.
El tiempo de demostración puede cambiar según el equipo utilizado.

## Comandos

Desde la raíz del repositorio, después de activar `.venv`:

```bash
# Experimento principal, gráficos, GIF y comparación:
MPLBACKEND=Agg python -m experiments.run_part1

# Demostración cronometrada (salidas separadas):
MPLBACKEND=Agg python -m experiments.run_part1 --config configs/part1_demo.yaml

# Pruebas:
MPLBACKEND=Agg python -m pytest -q
```

Para la comprobación principal se ejecutaron los cálculos con `--no-visuals`
y luego la regeneración con `--render-only`. La demostración se ejecutó con el
comando completo, integrando cálculo, guardado, gráficos, animaciones e informe.

El informe numérico comprobado se conserva en [resultados/report.md](resultados/report.md),
acompañado por el CSV, las configuraciones y las versiones de paquetes. El
informe se regenera también en `results/part1/comparisons/all/report.md`.

## Entregables externos

Esta verificación cubre el código, experimentos, visualizaciones y comparación
solicitados. No acredita publicación del blog, grabación de videos individuales,
ni ejecución en una máquina distinta. El historial de Git debe incorporar los
cambios antes de compartirlos; los resultados pesados se regeneran por comando.
