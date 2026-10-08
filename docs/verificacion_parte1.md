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

## Auditoría final y vista HTML — 7 de octubre de 2026

Revisión posterior a la entrega registrada arriba:

- Se contrastaron las 300 corridas principales guardadas: semillas 42–71,
  coordenadas finales frente a trayectorias, f final, estadísticas y equivalencia
  de costos. Las comprobaciones fueron satisfactorias.
- La suite ampliada pasó **103 pruebas en 40,02 s** con los `RuntimeWarning`
  tratados como errores. Después se añadió y aprobó una prueba del gradiente
  de Rastrigin frente a diferencias centrales en 2D/3D (el archivo de Rastrigin:
  2 pruebas aprobadas, una preexistente y una nueva). Total actual: 104 pruebas.
- La demo completa se volvió a ejecutar mediante su comando único: **36,19 s**,
  código de salida 0, 300 corridas, gráficas, GIF e informes Markdown y HTML.
  El tiempo es local y no acredita rendimiento en otros equipos.
- Se generaron `report.html` para el estudio principal, la demo y la copia
  `docs/resultados/`. Se comprobaron los 26 archivos visuales enlazados del
  informe principal: 20 PNG y 6 GIF legibles.
- Se validan parámetros en las llamadas directas a ambos GD: entero no negativo
  de iteraciones, tasa finita positiva y vector inicial finito con al menos dos
  coordenadas. Cero iteraciones sigue siendo válido para evaluar el inicio.
- El texto generado ya no atribuye los presupuestos principales a la demo.
- Se añadió fundamentación de convexidad local y condicionamiento, y un
  [registro de IA y verificaciones](uso_ia_y_verificaciones.md).

**Incidencia no reproducida:** en una ejecución anterior de esta auditoría falló
el renderizado de una prueba de GIF 3D. La prueba aislada, la suite completa
posterior y la demo con GIF 3D pasaron. No se identificó la causa ni se modificó
el renderizador: no se declara un arreglo no demostrado. Si reaparece, conservar
el traceback completo (la limpieza de Pillow puede ocultar la excepción inicial).

**Límite de la revisión visual HTML:** se verificaron estructura, datos y rutas
con pruebas, pero el navegador automatizado no estuvo disponible para inspección
visual; el intento de Chrome local quedó bloqueado por permisos del entorno.
Abrir el HTML en el navegador del equipo de sustentación forma parte del ensayo.

## Qué sigue, en orden

1. Abrir `results/part1/comparisons/all/report.html` y ensayar la explicación:
   función, gradiente, semilla, trayectoria, estadísticas y costos. Usar la demo
   para ejecutar en vivo y el informe principal para discutir resultados.
2. Revisar con el equipo el registro de IA. Incorporar sus prompts y hallazgos
   reales, conservando evidencias; la tabla de verificaciones no se presenta como
   cinco alucinaciones descubiertas.
3. Integrar metodología, resultados, bibliografía y uso de IA en el blog del
   equipo y publicarlo. Un HTML local no acredita publicación. Revisar APA 7 y
   numeración/referencias de todas las figuras y tablas del blog final.
4. Guardar estos cambios en Git, compartirlos y hacer el ensayo en un clon limpio
   **en otra máquina**, cronometrando la demo y registrando commit y entorno.
5. Grabar el video individual de 2–3 minutos con evidencia de contribución real,
   y practicar modificar un parámetro del YAML y anticipar su efecto.

La auditoría numérica de esta revisión se concentra en la Parte 1. No acredita
la calidad de los datos reales, los costos ni las fuentes de la Parte 2 (TSP).
No se puede afirmar que el trabajo completo cumple absolutamente todo mientras
falten esas verificaciones y las entregas externas.

## Ajuste del ritmo de las animaciones

- `pacing: movement` reparte el tiempo visual: 90% según desplazamiento y 10%
  según iteraciones. La interpolación se limita a segmentos entre estados
  consecutivos; el pie y la iteración aproximada `≈` lo declaran.
- El experimento principal usa 60 fotogramas a 5 fps; la demo, 48 a 4 fps.
  En ambos casos la reproducción dura 12 segundos para las corridas ilustradas.
- Pasaron 51 pruebas de animaciones e integración, incluidas pruebas nuevas
  que comprueban posiciones interpoladas, extremos, duración y conservación
  de resultados. Se inspeccionaron fotogramas de Rosenbrock 2D y 3D.
- Durante la regeneración visual se verificó por SHA-256 que todos los archivos
  `raw` de ambos estudios permanecieron intactos. Los parámetros de optimización
  y el criterio de selección de la corrida ilustrada no cambiaron.
- La versión inicial de 60 fotogramas tardó 129,33 s en regenerar la demo;
  por eso se redujo a 48 fotogramas manteniendo los 12 s de reproducción.
  Los tiempos anteriores de demo con 8 fotogramas son registros históricos,
  no mediciones de esta configuración visual nueva.
- La demo completa con la configuración final (48 fotogramas a 4 fps)
  terminó con código 0 en **117,06 s** en esta máquina. Queda cerca del límite
  de dos minutos: se debe cronometrar en el equipo de sustentación. Se verificaron
  los seis GIF de cada estudio: todos duran exactamente 12000 ms.
