# Uso de IA y Cacería de la alucinación

Este registro reúne la evidencia de asistencia de IA del trabajo. El equipo debe
complementarlo con sus otras conversaciones y revisar las afirmaciones antes
de incorporarlo al blog. No acredita que cada integrante haya escrito todo el
código sin ayuda ni sustituye la explicación individual en la sustentación.

## Sara Acevedo Maya — Rosenbrock y descenso por gradiente

****Alcance de este aporte:**** Rosenbrock 2D/3D, descenso por gradiente y sus
visualizaciones. Actualización documental: 9 de octubre de 2026.

### Prompts conservados e impacto

Los siguientes textos ya estaban transcritos en este archivo como prompts de
Sara. Se conserva su escritura original. No se recuperó la conversación
original con fechas, herramienta/modelo y respuestas completas; por eso las
descripciones de impacto son resúmenes documentados, no citas de la respuesta
de la IA ni una atribución de todos los archivos a un único prompt.

#### R01. Desarrollo incremental de Rosenbrock y GD

> Bien. Ahora implementemos únicamente el primer cambio necesario para Persona 1. Haz el cambio mínimo posible, explícame antes qué vas a modificar y después explícame línea por línea lo nuevo. No avances al siguiente requisito hasta comprobar que este funciona.

Impacto: desarrollo incremental de Rosenbrock y GD, con explicaciones y pruebas.

La responsabilidad de comprender y defender el código sigue siendo del equipo.

Evidencia relacionada: [función y gradiente](../src/optimization/rosenbrock.py),
[optimizador GD](../src/optimization/gradient_descent_rosenbrock.py) y
[ejecutor de Persona 1](../experiments/run_persona1.py). Las pruebas del
[gradiente y mínimo conocido](../tests/test_rosenbrock.py) y de
[trayectorias y contadores](../tests/test_gd_rosenbrock.py) permiten contrastar
la implementación. El código existente no prueba por sí solo qué fragmento
produjo la IA en respuesta a este mensaje.

#### R02. Presentación y dimensiones de las animaciones

> se ve un poco generico, haslo mas girly y solo se necesita animaciṕn en 2d?

Impacto: adaptación visual de las animaciones a una paleta rosa y lavanda.

La estética no cambia las trayectorias guardadas ni los contadores del algoritmo.

El enunciado inicial pedía animar GD y al menos un heurístico; la configuración
actual genera un GIF para cada método y cada dimensión, incluido 3D.

Evidencia relacionada: [animaciones](../visualization/animations.py) y
[pruebas de fidelidad de la visualización](../tests/test_animations.py).

En mi parte, la animación representa la trayectoria de GD sobre Rosenbrock.

Una superficie dibujada en tres ejes no implica que la función tenga tres
variables: hay que distinguir `z = f(x1,x2)` de los ejes `x1,x2,x3`.

#### R03. Ilustración de Rosenbrock de tres variables

> en el gif 3d me gustaria ver tambien la función ilustrada , no solo el recorrido y termina esto : ****El orden que recomiendo ahora:**** reparar el comando de Rastrigin; completar sus 30 corridas y estadísticas; integrar ambos problemas en los heurísticos con contadores y resultados; añadir una animación heurística; y redactar la comparación de costos y resultados.

Se conserva el mensaje completo para no alterar la evidencia. El aporte
documentado aquí se limita a la primera solicitud: representar la función de
tres variables junto al recorrido. Las solicitudes posteriores de integración
quedan fuera de este registro individual de Rosenbrock/GD.

Impacto en mi parte: incorporación de superficies de nivel `f=1` y `f=10` en
Rosenbrock 3D. Los ejes representan las tres coordenadas de entrada y el valor
de la función se muestra por separado. La función `rosenbrock_isosurface` de
[animations.py](../visualization/animations.py) implementa las dos ramas de
esas superficies. La verificación V01, más abajo, comprueba su significado.

### Discusión del impacto en mi entrega

Los prompts conservados muestran dos usos de la IA: acompañar el desarrollo
paso a paso del código y mejorar la interpretación visual de la trayectoria.

La solicitud de explicaciones línea por línea busca facilitar la comprensión;
no demuestra, por sí sola, el dominio del algoritmo. Los cambios visuales
tampoco validan los resultados matemáticos. Por eso se acompañan de pruebas
del gradiente, del mínimo conocido, de los contadores y de las superficies de
nivel. En la sustentación corresponde explicar esas comprobaciones, la regla
`x_nuevo = x − α∇f(x)` y las limitaciones del paso fijo.

### Ivan Dario Gomez Cabrera - Descenso por gradiente (GD) para Rastrigin
****Alcance de este aporte:****Implementación y evaluación del algoritmo de descenso por gradiente para optimizar la función Rastrigin en dos y tres dimensiones, utilizando condiciones iniciales aleatorias, una tasa de aprendizaje de 0.001 y un máximo de 10.000 iteraciones. Se realizaron 30 corridas por dimensión y se analizaron los resultados obtenidos mediante estadísticas y gráficas de convergencia.

### Prompts conservados e impacto
El siguiente prompt se preparó para representar una consulta de orientación sobre la implementación del algoritmo. No se afirma que se haya enviado literalmente a la IA, salvo que exista un registro verificable de la conversación.

#### I01. Orientación para implementar el algoritmo evolutivo
>Necesito implementar en Python un algoritmo de descenso por gradiente para optimizar la función Rastrigin en dos y tres dimensiones, partiendo de condiciones iniciales aleatorias. ¿Me puedes explicar cómo calcular el gradiente, implementar las actualizaciones de las coordenadas, organizar las corridas experimentales y representar gráficamente el proceso de optimización?

Impacto previsto: Comprender el funcionamiento del descenso por gradiente, calcular el gradiente analítico de Rastrigin y estructurar la implementación para ejecutar experimentos reproducibles. También se busca analizar el comportamiento del algoritmo frente a los mínimos locales de la función y representar su convergencia mediante gráficas.

Evidencia relacionada: Implementación del descenso por gradiente, función Rastrigin y su gradiente, configuración de la Parte 1, ejecutor de experimentos y las figuras y resultados generados durante las corridas. Estos archivos permiten verificar la implementación y los resultados, pero no demuestran por sí solos que el prompt propuesto haya sido enviado.

#### I02. Verificación de compatibilidad e integración del código

>Quiero que me verifiques si mi código se acopla con los demás archivos necesarios del proyecto.

Impacto: La consulta estuvo orientada a revisar la integración de la implementación del descenso por gradiente para Rastrigin con los demás componentes del repositorio. Esto incluye comprobar la compatibilidad de las importaciones, la estructura de los módulos, los parámetros de configuración, el formato de los resultados y la conexión con el ejecutor de experimentos y las herramientas de análisis estadístico.

Esta revisión permite identificar posibles incompatibilidades entre la implementación del algoritmo y los archivos existentes, facilitando su integración en el flujo general de experimentación. La verificación debe respaldarse con la revisión del código y, cuando corresponda, con la ejecución de pruebas.

Evidencia relacionada: src/optimization/gradient_descent_rastrigin.py, src/optimization/rastrigin.py, configs/part1.yaml, experiments/run_part1.py y los archivos de pruebas correspondientes. Estos archivos permiten documentar la estructura revisada y comprobar la integración mediante su ejecución.

### Discusión del impacto en mi entrega

En mi parte del proyecto implementé el algoritmo de descenso por gradiente para minimizar la función Rastrigin en dos y tres dimensiones. La implementación utiliza el gradiente analítico para actualizar iterativamente las coordenadas en dirección contraria al gradiente, con el objetivo de reducir el valor de la función. Se incorporaron registros de la trayectoria, contadores de evaluaciones, validaciones numéricas y detección de divergencias.

La evaluación se realizó mediante 30 corridas por dimensión, utilizando semillas desde 42 hasta 71, una tasa de aprendizaje de 0.001 y un máximo de 10.000 iteraciones por corrida. Los resultados mostraron un valor final promedio de 15.8197 en dos dimensiones y de 24.4758 en tres dimensiones. En ambos casos, se obtuvo una tasa de éxito del 0 %, considerando como criterio alcanzar un valor de la función menor o igual a 0.0001.

Estos resultados evidencian una limitación del descenso por gradiente frente a la estructura multimodal de Rastrigin, que presenta numerosos mínimos locales. El algoritmo puede converger hacia un mínimo local dependiendo de la condición inicial, sin alcanzar necesariamente el mínimo global. La comparación con métodos poblacionales, como la evolución diferencial y la optimización por enjambre de partículas, permitió observar diferencias en la exploración del espacio de búsqueda para las configuraciones evaluadas.

Finalmente, las estadísticas y gráficas de convergencia permitieron documentar el comportamiento del algoritmo y analizar sus resultados. La orientación mediante inteligencia artificial se distingue del trabajo de implementación, ejecución y verificación de los experimentos realizados en el repositorio.

## Nicole Guaranguay — Algoritmo evolutivo

****Alcance de este aporte:**** Implementación del algoritmo evolutivo para optimizar Rosenbrock y Rastrigin en 2D y 3D, con selección por torneo, cruce BLX-alpha, mutación gaussiana y elitismo.

### Prompts conservados e impacto

El siguiente prompt se preparó para representar una consulta inicial de orientación sobre el algoritmo. A diferencia de los prompts transcritos de Sara, **no se ha comprobado que este texto se enviara literalmente a la IA**. Se presenta como prompt propuesto y no como registro histórico de una conversación.

#### N01. Orientación para implementar el algoritmo evolutivo

> Necesito implementar un algoritmo evolutivo en Python para optimizar las funciones Rosenbrock y Rastrigin. ¿Me puedes explicar cómo funciona, qué métodos de selección, cruce y mutación puedo utilizar y cómo podría organizar el código para implementarlo correctamente?

Impacto previsto: comprender las etapas del algoritmo evolutivo y organizar el código para desarrollar los operadores de selección, cruce y mutación, así como el mecanismo de elitismo. Este texto documenta el propósito de la consulta, pero no acredita una respuesta concreta de IA.

Evidencia relacionada: [algoritmo evolutivo](../src/optimization/evolutionary.py), [configuración de la Parte 1](../configs/part1.yaml), [ejecutor de experimentos](../experiments/run_part1.py) y [pruebas del evolutivo](../tests/test_evolutionary.py). Estos archivos permiten comprobar la implementación y sus resultados, no demostrar que el prompt propuesto haya sido enviado.

### Discusión del impacto en mi entrega

En mi parte del proyecto implementé el algoritmo evolutivo y evalué su comportamiento en las funciones Rosenbrock y Rastrigin para dos y tres dimensiones. La selección por torneo permite elegir los padres; el cruce BLX-alpha genera nuevas soluciones; la mutación gaussiana introduce variaciones, y el elitismo conserva los mejores individuos. Las corridas y las pruebas del repositorio permiten revisar el desempeño obtenido y el conteo de evaluaciones. El uso de IA como orientación debe distinguirse de la implementación y verificación efectivamente realizadas.


## Nicolás Ruiz - Optimización de Hiperparametros, Evolución Diferencial

**Alcance de este aporte:** selección de hiperparámetros mediante Grid Search,
integración de las configuraciones 2D/3D, ejecución de Evolución Diferencial
(DE), persistencia de resultados y actualización de benchmarks e informes.

### Prompts conservados e impacto

Cuando no se conserva la respuesta literal de la IA, el impacto se documenta
con base en los archivos y resultados verificables. No se atribuyen a una
conversación concreta fragmentos que no estén disponibles.

#### NR01. Integración completa de la tercera dimensión

> Extiende el experimento existente de 2D a 3D para todas las funciones y todos
> los métodos. Integra la nueva dimensión en la configuración, ejecución,
> visualizaciones, animaciones, benchmarks e informes, sin modificar los tests.

Impacto: la configuración y el flujo de ejecución se ampliaron para Rosenbrock
y Rastrigin con GD, PSO, evolutivo y DE en 2D y 3D. El informe principal reúne
16 configuraciones y conserva separadas las salidas de la demo.

Evidencia relacionada: [configuración](../configs/part1.yaml),
[ejecutor](../experiments/run_part1.py),
[comparación](../src/optimization/comparison.py),
[DE](../src/optimization/differential_evolution.py) y
[verificación de Parte 1](verificacion_parte1.md).

#### NR02. Selección y documentación de hiperparámetros

> Documenta el proceso de Grid Search, los valores seleccionados para cada
> método y la validación final. Explica las limitaciones de la búsqueda y no
> presentes los parámetros como óptimos universales.

Impacto: se documentó la exploración previa con semillas 42, 43 y 44, un
presupuesto reducido y la validación final con 30 corridas por configuración.
La configuración consolidada se dejó explícita en el YAML y en el informe.

Evidencia relacionada: [justificación de parámetros](<Justificacion%20de%20parametros.md>),
[metodología](parte1_metodologia.md), [YAML principal](../configs/part1.yaml) y
[reporte de resultados](resultados/report.md).

#### NR03. Persistencia y regeneración de resultados

> Asegura que los resultados de las ejecuciones filtradas, especialmente las
> configuraciones 3D, se incorporen al `report.md`, `comparison.csv` y
> `comparison.json` globales. Debe ser posible regenerar el informe sin repetir
> las optimizaciones.

Impacto: el flujo reconstruye el informe global desde los resultados
persistidos y permite regenerar tablas y visualizaciones con `--render-only`.
Esto evita confundir un informe filtrado con el estudio completo.

Evidencia relacionada: [run_part1.py](../experiments/run_part1.py),
[reporte Markdown](resultados/report.md),
[CSV](resultados/comparison.csv) y [JSON](resultados/comparison.json).

#### NR04. Instalación reproducible con UV

> Propón una forma general y reproducible de crear el entorno del proyecto con
> UV, respetando la versión de Python y las dependencias fijadas. Incluye
> comandos de comprobación y explica qué hacer si UV o el acceso a paquetes no
> están disponibles.

Impacto: este prompt se añade como documentación general de reproducibilidad.
La receta debe verificarse contra `.python-version`, `requirements.txt` y la
salida real de las pruebas; un comando de instalación por sí solo no demuestra
que el entorno esté correctamente reproducido.

Evidencia relacionada: [.python-version](../.python-version),
[requirements.txt](../requirements.txt), [README](../README.md) y
[verificación de Parte 1](verificacion_parte1.md).

### Discusión del impacto en mi entrega

La IA se utilizó como apoyo para estructurar la ampliación a 3D, documentar la
selección de hiperparámetros y revisar la persistencia de resultados. La
implementación final se contrastó con el YAML, los contadores, los archivos
generados y las pruebas disponibles. En particular, la comparación entre
métodos debe considerar los presupuestos reales y no solo el número nominal de
generaciones.

## Sebastián Cataño — PSO y revisión del TSP

### Alcance del aporte y uso de IA

Se utilizó Claude como apoyo para desarrollar la implementación de optimización por enjambre de partículas PSO. Posteriormente, se utilizó ChatGPT/Codex para revisar el proyecto, actualizar los resultados del TSP, corregir sus visualizaciones y realizar un análisis de sensibilidad a los peajes provisionales.

### Prompts reconstruidos para PSO

**P01. Implementación del algoritmo**

> Desarrolla una implementación modular de PSO en Python con NumPy para minimizar Rosenbrock y Rastrigin en dos y tres dimensiones. La función debe permitir configurar el dominio, el tamaño del enjambre, las iteraciones, la semilla y los coeficientes de actualización. Explica la inicialización de las partículas y la relación entre las ecuaciones matemáticas y el código.

Relación con el proyecto: función `run_pso`, inicialización aleatoria y actualización de velocidades y posiciones en `src/optimization/pso.py`.

**P02. Gestión de las mejores soluciones**

> Revisa la actualización de la mejor posición individual y de la mejor posición global del enjambre. Verifica que se conserven las mejoras, que las copias de los arreglos eviten modificaciones involuntarias y que los factores aleatorios se generen independientemente para cada partícula y coordenada.

Relación con el proyecto: manejo de `p_best`, `p_best_val`, `g_best` y los factores aleatorios `r1` y `r2`.

**P03. Reproducibilidad y conteo de evaluaciones**

> Instrumenta el algoritmo para registrar todas las evaluaciones de la función objetivo, incluida la evaluación inicial del enjambre. Comprueba que el conteo corresponda a N_f = P(T + 1) y utiliza semillas configurables para reproducir las corridas de forma independiente.

Relación con el proyecto: generador `numpy.random.default_rng(seed)` e historial de evaluaciones. Con 40 partículas y 999 iteraciones, PSO realiza 40.000 evaluaciones.

**P04. Persistencia de resultados y visualización**

> Estructura la salida del optimizador para conservar la evolución del mejor punto, sus valores objetivo, las evaluaciones acumuladas y las posiciones de todas las partículas. Los historiales deben permitir regenerar gráficas y animaciones sin repetir la optimización y distinguir el movimiento del enjambre de la trayectoria del mejor punto conocido.

Relación con el proyecto: historiales `trajectory`, `values_history`, `evaluations` y `population_history`.

### Consultas de TSP — versiones editadas para presentación

**T01. Actualización de resultados y sincronización del blog**

> Revisa la implementación local del TSP y regenera los resultados de ACO y del algoritmo genético utilizando las matrices viales y configuraciones vigentes. Actualiza los resúmenes, mapas, animaciones y tablas del blog. Comprueba la coherencia entre los costos de optimización, sus desgloses y el estudio del valor de la hora, conservando los resultados publicados de la Parte 1.

Impacto comprobado: actualización de los resultados principales e incorporación de `--tsp-only` para sincronizar únicamente el TSP.

Evidencia: commit `39ef0d0`, `docs/datos/resultados_blog.json` y `scripts/build_blog.py`.

**T02. Representación geográfica de las rutas**

> Corrige las gráficas y animaciones del TSP para representar los recorridos sobre un mapa geográfico de España. Incorpora los límites territoriales como fondo, conserva la correspondencia con las coordenadas de las capitales y almacena los recursos necesarios para que las visualizaciones puedan regenerarse sin conexión a internet.

Impacto comprobado: incorporación del mapa de fondo y regeneración de las visualizaciones de ACO y GA. Las líneas representan el orden de visita entre capitales; las distancias y tiempos se obtienen de las matrices viales.

Evidencia: commit `5e35faf`, `visualization/plot_tsp.py`, `data/tsp/iberia_boundaries.geojson` y `docs/imagenes/tsp/`.

**T03. Análisis de sensibilidad a los peajes provisionales**

> Evalúa una alternativa reproducible para estudiar la influencia de los peajes sin verificar individualmente todos los trayectos. Implementa escenarios que excluyan, mantengan y dupliquen los importes provisionales registrados. Ejecuta ambos algoritmos con semillas emparejadas, reporta costos y cambios de ruta, y distingue el efecto directo del precio de la variabilidad asociada a volver a optimizar.

Impacto comprobado: ejecución de 18 corridas con factores de peaje 0, 1 y 2, utilizando tres semillas por algoritmo. Se publicaron estadísticas y se recalcularon las rutas base manteniendo fijo su recorrido.

Evidencia: commit `a6304af`, `experiments/run_toll_study.py`, `tests/test_toll_study.py` y `docs/datos/sensibilidad_peajes.json`.

### Discusión del impacto y límites

La IA sirvió como apoyo para estructurar el código, revisar resultados y preparar experimentos reproducibles. La validación incluyó pruebas automatizadas, comprobaciones de costos y revisión de las visualizaciones.

El análisis de sensibilidad permite estudiar el comportamiento del modelo bajo distintos supuestos. No verifica tarifas oficiales ni completa los peajes desconocidos. Tampoco demuestra optimalidad global o superioridad general de un algoritmo.

## Cacería de la alucinación: verificaciones con evidencia

El enunciado permite documentar verificaciones si no se encuentran cinco

hallazgos genuinos. No disponemos aquí de cinco respuestas incorrectas literales

con evidencia suficiente para atribuirlas a la IA. Por eso los siguientes son

****controles realizados****, no cinco alucinaciones inventadas.

Las fichas V01 y V02 desarrollan controles que ya aparecían en la tabla

general: representación de Rosenbrock 3D y costo equivalente de GD. Se añaden

experimentos reproducibles y resultados del 9 de octubre de 2026. **Son dos

verificaciones documentadas de la tarea de Sara, no dos respuestas erróneas

de IA demostradas.** Si se recuperan esas respuestas originales, podrán

completarse los campos de atribución sin reconstruir citas de memoria.

### V01. Distinguir Rosenbrock 3D de una superficie de Rosenbrock 2D

**Responsable:** Sara Acevedo Maya. V01 y V02 se comprobaron de nuevo el 13 de octubre de 2026 y se desarrollaron también en la [sección de Cacería del blog](index.html#sara-v01). Continúan clasificadas como verificaciones: no se recuperó una respuesta literal incorrecta de IA.

**Categoría:** matemáticas y representación de funciones.

1. **Prompt conservado:** R03, transcrito completo arriba. La parte pertinente solicita ilustrar la función en el GIF 3D, además de mostrar el recorrido.
2. **Respuesta relevante de IA:** no se conserva una respuesta literal que contenga un error. La afirmación que se pone a prueba —no una cita de IA— es que dibujar `z=f(x1,x2)` bastaría para representar Rosenbrock de tres variables.
3. **Motivo de la comprobación:** la altura de una superficie 2D es el valor de la función; la tercera coordenada de Rosenbrock 3D es otra variable de entrada. Confundirlas cambia el objeto matemático que se está mostrando.
4. **Evidencia:** con la implementación del proyecto, `f(-1.2,1)=24.2`, mientras que `f(-1.2,1,0.5)=49.2`. El término asociado a la tercera variable no se puede omitir. Para construir niveles reales de la función 3D se despeja:

   ```text
   A = 100(x2 − x1²)² + (1 − x1)² + (1 − x2)²
   x3 = x2² ± sqrt((c − A)/100), cuando A ≤ c.
   ```

   En `x1=x2=1`, los puntos con `x3=0.9` y `x3=1.1` dan `f≈1`; con `x3≈0.683772234` y `x3≈1.316227766` dan `f≈10`. El [JSON de evidencia](evidencias_ia/rosenbrock_verificaciones.json) conserva los valores completos. La prueba `test_isosurfaces_are_actual_rosenbrock_level_sets` comprueba además puntos de una malla para ambos niveles.
5. **Conclusión y representación correcta:** una superficie `z=f(x1,x2)` representa una función de dos variables. Para el GIF de Rosenbrock 3D, los ejes son `x1,x2,x3`, las superficies corresponden a `f=c` y el valor objetivo se muestra aparte. El código actual ya implementa esta representación; esta ficha no afirma haber encontrado y corregido ahora una respuesta de IA equivocada.
6. **Lección:** comprobar las variables de entrada y sustituir puntos de la visualización en la función original. Una gráfica atractiva no basta para demostrar que representa la función correcta.

### V02. Separar llamadas reales y costo equivalente del gradiente

**Categoría:** código y conceptos de comparación de costos.

1. **Prompt conservado de contexto:** R01, sobre desarrollo incremental y comprobación del código de Persona 1. No se conserva un prompt específico que pidiera la afirmación cuestionada sobre costos.
2. **Respuesta relevante de IA:** no se conserva una respuesta literal incorrecta. La afirmación que se contrasta —no una cita de IA— es que `C=N_f+2d·N_grad` corresponde al número de llamadas reales a `f` que realiza GD con gradiente analítico.
3. **Motivo de la comprobación:** diferencias centrales requieren dos evaluaciones por coordenada; una fórmula analítica de gradiente no tiene por qué llamar a `f`. Confundir ambas formas de cálculo atribuiría al optimizador evaluaciones que no ejecutó.
4. **Evidencia:** se instrumentaron las funciones con contadores de llamadas independientes del contador del optimizador, usando diez iteraciones y paso `0.001`. Los resultados se muestran en la Tabla 1.

**Tabla 1. Conteo real frente al costo equivalente de GD-Rosenbrock.**

Fuente: ejecución de `docs/evidencias_ia/verificar_rosenbrock.py`, 9 de octubre de 2026; resultados en [rosenbrock_verificaciones.json](evidencias_ia/rosenbrock_verificaciones.json).

| Dimensión | Punto inicial        | Iteraciones | Llamadas reales a\(f\) | Llamadas reales al gradiente | Costo equivalente |
| ---------: | -------------------- | ----------: | ---------------------: | ---------------------------: | ----------------: |
|          2 | `(-1.2, 1.0)`      |          10 |                      1 |                           10 |                41 |
|          3 | `(-1.2, 1.0, 0.5)` |          10 |                      1 |                           10 |                61 |

5. **Conclusión e interpretación correcta:** GD evalúa `f` una vez al final y utiliza diez evaluaciones de su gradiente analítico en estos ejemplos. Los valores 41 y 61 son costos equivalentes bajo la convención declarada, no llamadas reales a `f` ni segundos de ejecución. Las evaluaciones para dibujar figuras se contabilizan fuera de la optimización. El conteo actual es consistente; se documenta una verificación, no un defecto corregido.
6. **Lección:** instrumentar las llamadas, reportar `N_f` y `N_grad` por separado y explicar la equivalencia. No deducir el costo real de una etiqueta, del número de fotogramas ni del número de iteraciones solamente.

### V03. Interpretación apresurada de la mejora del algoritmo evolutivo — Nicole Guaranguay

**Categoría:** interpretación de resultados y razonamiento causal.

1. **Contexto y consulta conservada:** durante el ajuste del algoritmo evolutivo se preguntó: «Si se obtiene que sí es por esos valores que se debería realizar?». La consulta hacía referencia a los valores de mutación y elitismo que podían estar afectando la convergencia.
2. **Afirmación que motivó la verificación:** al comparar los resultados exploratorios, la IA presentó la reducción del elitismo como principal explicación de la mejora en Rosenbrock 3D. La conclusión era demasiado firme para el diseño del experimento, porque además cambiaron las generaciones y el número de descendientes por generación.
3. **Por qué se cuestionó:** pasar del 50 % al 20 % de élite implica conservar 20 frente a 8 individuos y producir 20 frente a 32 hijos nuevos por generación. La configuración óptima consolidada establece 1249 generaciones, con 40008 evaluaciones. Por ello, los ensayos compararon configuraciones completas, no el efecto aislado de una variable manteniendo constante todo lo demás.
4. **Evidencia:** las siguientes salidas fueron compartidas durante los experimentos de 30 corridas por configuración, con umbral de éxito de 0,0001:

   | Prueba             | Élite | Sigma | Generaciones | Evaluaciones | Éxitos Rosenbrock 3D |
   | ------------------ | -----: | ----: | -----------: | -----------: | --------------------: |
   | Original           |   50 % |  0,10 |         1998 |       40.000 |                  0/30 |
   | A: menor mutación |   50 % |  0,05 |         1998 |       40.000 |                  0/30 |
   | B: menor elitismo  |   20 % |  0,10 |         1248 |       39.976 |                  9/30 |
   | C: ambos cambios   |   20 % |  0,05 |         1248 |       39.976 |                  6/30 |

   La diferencia entre 40.000 y 39.976 evaluaciones es de 24 llamadas, equivalente al 0,06 %. Las salidas de terminal y el fragmento de conversación original pueden incorporarse como capturas de respaldo; **no se adjuntan capturas que no estén disponibles**.
5. **Corrección:** la prueba B obtuvo mejores resultados observados que la configuración original, pero eso demuestra una mejora de la configuración probada, **no que el elitismo por sí solo sea la causa exclusiva**. Una afirmación causal más fuerte exigiría controlar también cómo se distribuyen las evaluaciones a lo largo de las generaciones y repetir experimentos comparables.
6. **Lección aprendida:** las explicaciones de la IA deben confrontarse con el diseño de los experimentos y sus salidas reales. Las tasas de éxito, por sí solas, no identifican qué parámetro es responsable de una mejora.

**Diferencia respecto de la entrega principal:** esta tabla corresponde a ensayos exploratorios. La configuración definitiva usa 40 individuos, 1249 generaciones, BLX-α = 0,6 y elitismo del 20 %, con **40.008 evaluaciones por corrida**. El número de generaciones se ajustó después de seleccionar los hiperparámetros óptimos para aproximar el presupuesto objetivo de 40 000 evaluaciones. No deben mezclarse los resultados de ambas configuraciones.

### V04. El algoritmo evolutivo no usa 40 000 evaluaciones con una élite de 0.2

**Categoría:** costos, configuración experimental y comparación de métodos.

1. **Prompt:** «Documenta los parámetros finales de todos los métodos y verifica que los presupuestos de evaluación reportados coincidan con la configuración realmente ejecutada».
2. **Respuesta de la IA:** No se identificó la afirmación incorrecta de que el algoritmo evolutivo usaba 40 000 evaluaciones, igual que PSO y DE, aunque la configuración final tenía una fracción de élite de 0.2. Lo que ocasiono que se informara de un numero que en realidad era muy distinto, pues con los parametros establecidos se hacian 63 976 evaluaciones
3. **Motivo de comprobación:** con población \(P=40\), fracción de élite \(0.2\), \(E=8\) individuos élite y \(G=1998\) generaciones, cada generación produce \(P-E=32\) hijos, no 20.
4. **Evidencia:** el cálculo ejecutado era:

   $$
   N_f = P + (P-E)G = 40 + (40-8)\cdot 1998 = 63\,976.
   $$

   La configuración final informaba 63 976 evaluaciones para el evolutivo y la Tabla 2 de [report.md](resultados/report.md) muestra ese valor en sus cuatro configuraciones. PSO y DE registran 40 000 evaluaciones.
5. **Conclusión:** con una élite de 0.2, 40 individuos y 1998 generaciones, el valor correcto es 63 976, por lo que fue necesario cambiar las generaciones a 1249 para que las evaluaciones totales dieran **40008**. La diferencia de ocho evaluaciones respecto al presupuesto nominal se debe a que cada generación produce 32 hijos y las generaciones deben ser enteras. La configuración óptima y el informe fueron actualizados para reflejar este cambio.
6. **Lección:** los presupuestos deben calcularse desde las reglas de reproducción del algoritmo y contrastarse con los contadores guardados; no se debe asumir que todos los métodos tienen el mismo costo por usar poblaciones de igual tamaño.

### Reproducción de las evidencias de Sara

Desde la raíz del repositorio, con el entorno instalado:

```bash

MPLBACKEND=Agg .venv/bin/python docs/evidencias_ia/verificar_rosenbrock.py
```

El script verifica ambos casos y guarda los resultados en

`docs/evidencias_ia/rosenbrock_verificaciones.json`, junto con fecha y hashes

de los archivos utilizados. No modifica algoritmos ni resultados principales.

Como contraste adicional, se ejecutó:

```bash

MPLBACKEND=Agg .venv/bin/python -m pytest -q tests/test_rosenbrock.py tests/test_gd_rosenbrock.py::test_gd_rosenbrock_counts_actual_evaluations tests/test_part1.py::test_isosurfaces_are_actual_rosenbrock_level_sets

```

Resultado el 9 de octubre de 2026: ****12 pruebas aprobadas en 4,67 s****.

Es el resultado de esta selección de pruebas; no acredita que toda la suite

del proyecto pase. Las evidencias fueron ejecutadas con asistencia del agente

y no se atribuyen automáticamente a una ejecución manual de la estudiante.

### Registro general de verificaciones de Parte 1

La siguiente tabla conserva el registro previo del equipo; V01 y V02 amplían

dos de sus controles para la parte de Sara. Las menciones a pruebas o arreglos

en este registro histórico no certifican el estado actual de todos los métodos.

| Categoría   | Afirmación puesta a prueba                                    | Evidencia y resultado                                                                                                                                        | Lección                                                                                          |
| ------------ | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| Matemáticas | El gradiente implementado corresponde a cada función.         | Las pruebas de funciones contrastan derivadas analíticas con diferencias finitas en 2D/3D. Pasan en la suite.                                               | Comprobar derivadas numéricamente además de derivarlas.                                         |
| Matemáticas | La superficie del GIF representa Rosenbrock de tres variables. | `test_isosurfaces_are_actual_rosenbrock_level_sets` sustituye sus puntos y verifica \(f=1\) y \(f=10\).                                                    | En tres variables,\(z\) no debe confundirse con \(f\); hay que indicar qué representan los ejes. |
| Código      | Los contadores reflejan llamadas realmente ejecutadas.         | `test_population_counts_history_and_reproducibility` instrumenta el objetivo; las pruebas de GD comprueban sus contadores separados.                       | Contar llamadas dentro del optimizador, no deducirlas de una gráfica.                            |
| Código      | La visualización reproduce los datos guardados.               | `test_gif_preserves_endpoints_and_saved_data` compara cada punto animado y verifica que no se alteren archivos de resultados.                              | Separar cálculo, persistencia y visualización.                                                  |
| Conceptos    | Completar iteraciones equivale a encontrar el mínimo global.  | No: GD Rastrigin principal completa corridas pero obtiene 0/30 éxitos en cada dimensión al umbral 0.0001. Ver[comparison.json](resultados/comparison.json). | Separar`completed` de éxito, e informar \(f_{\mathrm{final}}\) y el umbral.                    |
| Conceptos    | \(C=N_f+2dN_{\mathrm{grad}}\) mide tiempo real.                | No: es una equivalencia justificada por diferencias centrales; el código usa gradientes analíticos. Ver metodología y contadores.                         | Declarar la convención y no interpretarla como un cronómetro.                                   |

En la auditoría también se encontraron parámetros inválidos aceptados por las

llamadas directas de GD (iteraciones negativas o tasa cero) y una explicación

confusa del presupuesto en el informe demo. Se agregaron validaciones y se

eliminó la referencia fija al presupuesto principal del informe generado. No

se atribuyen estos defectos a una respuesta literal de IA no conservada aquí.

Para añadir un hallazgo real, conservar: prompt literal, fragmento literal de

respuesta, sospecha, evidencia, corrección y lección. El equipo debe aportar

los hallazgos verificables de sus otras partes, si existen. No reconstruir citas

de memoria ni presentar esta tabla como cinco errores descubiertos.

## Guía para integrar aportes de otros integrantes

Cada integrante debe añadir un apartado con su **nombre y algoritmo**, siguiendo la estructura de Sara y Nicole: **alcance del aporte**, **prompts conservados e impacto**, **evidencia relacionada** y **discusión del impacto**. Se deben distinguir los prompts textuales recuperados de ejemplos preparados posteriormente.

Si identificó una afirmación incorrecta o una verificación técnica real, debe añadir una ficha consecutiva **V04, V05, etc.** con categoría, prompt literal cuando exista, afirmación revisada, motivo de sospecha, procedimiento y evidencia, corrección y aprendizaje. No se deben inventar capturas, prompts ni errores.

**Integración al blog:** en `docs/index.html`, sección 4, incluir un párrafo breve con el nombre, el propósito de cada consulta y la conclusión principal de cada verificación. El detalle y la evidencia permanecen en este Markdown. Para evitar conflictos, conviene que una sola persona integre el HTML después de recibir los aportes de todos.
