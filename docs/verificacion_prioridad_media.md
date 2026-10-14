# Verificación de los pendientes de prioridad media del TSP

Fecha de revisión: 13 de octubre de 2026. Alcance: TSP y sus secciones de
documentación y blog. No se modifican código, configuraciones, figuras ni
resultados publicados de la Parte 1, incluido PSO y el trabajo de otros integrantes.

## Cambios completados

1. **Valor de la hora.** Barrido de 0, 1, 2, 5, 10, 25, 50, 75 y 100 €/h,
   con las semillas 42, 43 y 44 en cada algoritmo: 54 corridas guardadas.
   Cada semilla se compara consigo misma mediante arcos dirigidos. Se conservan
   todas las rutas, media, desviación muestral, mejor costo y semilla ganadora.
   El primer cambio observado en ambos algoritmos aparece al pasar de 0 a
   1 €/h, en 3/3 semillas: intervalo de muestreo (0, 1] €/h. No constituye
   un umbral óptimo global ni separa por completo el efecto del azar.
2. **Dirección de las rutas.** ACO deposita feromona solo sobre los arcos
   recorridos, incluido el cierre, tanto en el depósito ordinario como en el
   elitista. La comparación de recorridos conserva la dirección; una rotación
   es equivalente y una inversión puede tener otro costo. Se actualizaron
   las ecuaciones y explicaciones que describían depósito en ambos sentidos.
3. **Matriz total archivada.** `data/tsp/total_cost_matrix.npz` conserva el
   costo total y los componentes monetarios a 25 €/h y factor de peajes 1.
   El JSON adjunto registra unidades, parámetros, orden de las 47 ciudades
   y hashes de entradas y salida. `python -m scripts.export_tsp_costs`
   la regenera sin internet. Los experimentos siguen calculando la matriz
   con sus propios parámetros, para evitar usar la base en otra tarifa.
4. **Referencias de datos.** Se añadieron al texto y a la bibliografía
   Natural Earth y OpenStreetMap, con fuentes, licencia y fecha de consulta;
   se conservaron las referencias verificadas de ORS, SEAT y MITECO.
   Las 47 coordenadas se contrastaron con GeoNames, conservando evidencia,
   identificadores y hashes. Las correspondencias de nombres se revisaron:
   separación máxima 1,607036 km entre referencias urbanas. Es una comprobación
   independiente, no una atribución del origen histórico del CSV.

## Validación realizada

- Antes de incorporar las actualizaciones remotas de otros integrantes, la
  suite completa aprobó **128 pruebas**. Después de integrar `ed7478c`
  (sin modificar sus archivos), el resultado es **127 aprobadas y 1 fallida**:
  `tests/test_part1.py::test_suite_covers_requirements_and_equivalent_budget`.
  Ese commit cambia las generaciones del evolutivo en `configs/part1.yaml`
  de 1998 a 1249; la aserción existente del presupuesto ya no coincide.
  No se modifica ni la configuración ni esa prueba, por quedar fuera del TSP.
- Todas las pruebas específicas del TSP aprueban: **14 pruebas**, mediante
  `python -m pytest -q tests/test_tsp.py tests/test_toll_study.py tests/test_tsp_directed_study.py`.
  Incluyen regresiones de depósito dirigido, cierre del ciclo, comparación
  entre semillas iguales y exportación de costos con parámetros distintos
  de los predeterminados.
- Dos ejecuciones principales completas con mapas y GIF; a 25 €/h, semilla
  42 y factor 1: ACO **2546,56 €**, GA **2561,25 €**. Cada recorrido visita las
  47 ciudades una vez y regresa al inicio. Se comprobó que estas rutas coinciden
  con sus corridas emparejadas del barrido.
- 54 corridas del valor de la hora y 18 de peajes contrastadas contra las
  matrices originales y la fórmula del costo; medias, desviaciones y costos
  de rutas base recalculados de forma independiente.
- Comprobación de sincronización de imágenes y datos del blog, apertura de
  PNG/GIF y existencia de las 52 figuras. Revisión visual del nuevo mapa ACO.
- Sintaxis JavaScript y ejecución de las tablas dinámicas con un DOM simulado:
  nueve filas horarias, seis escenarios de peajes e interpretación de intervalos.
  Esto no equivale a una inspección visual del blog completo en un navegador.
- Los datos publicados de la Parte 1 se compararon con la versión anterior
  y permanecen iguales. Las imágenes de la Parte 1 no forman parte del cambio.

## Reproducción

Desde la raíz del repositorio, con el entorno instalado:

```powershell
python -m pytest -q
python -m experiments.run_tsp --config configs/tsp_aco.yaml
python -m experiments.run_tsp --config configs/tsp_ga.yaml
python -m experiments.run_tsp --config configs/tsp_aco.yaml --study-hourly-rates
python -m experiments.run_tsp --config configs/tsp_ga.yaml --study-hourly-rates
python -m experiments.run_toll_study
python -m scripts.export_tsp_costs
python -m scripts.build_blog --tsp-only
```

Para repetir el contraste geográfico, descargar `ES.zip` desde GeoNames y
ejecutar `python -m scripts.verify_tsp_coordinates --archive ruta/ES.zip`.
Revisar las correspondencias antes de publicar la nueva evidencia; el proveedor
puede actualizar los datos y cambiar el hash de la descarga.

Los peajes siguen siendo provisionales. Se conservan los escenarios 0, 1 y 2
con sus límites metodológicos; no se han integrado los archivos de investigación
de peajes que se pidió dejar fuera. Esta verificación no certifica tarifas
reales, optimalidad global ni cumplimiento de los entregables de video o demo.
