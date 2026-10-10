# Uso de IA y Cacería de la alucinación — Parte 1

Este registro reúne la evidencia de asistencia de IA del trabajo. El equipo debe
complementarlo con sus otras conversaciones y revisar las afirmaciones antes
de incorporarlo al blog. No acredita que cada integrante haya escrito todo el
código sin ayuda ni sustituye la explicación individual en la sustentación.

## Sara Acevedo Maya — Persona 1: Rosenbrock y descenso por gradiente

**Alcance de este aporte:** Rosenbrock 2D/3D, descenso por gradiente y sus
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
El enunciado pide animar GD y al menos un heurístico; no exige expresamente un
GIF separado para cada dimensión. El proyecto incluye también GD 3D.

Evidencia relacionada: [animaciones](../visualization/animations.py) y
[pruebas de fidelidad de la visualización](../tests/test_animations.py).
En mi parte, la animación representa la trayectoria de GD sobre Rosenbrock.
Una superficie dibujada en tres ejes no implica que la función tenga tres
variables: hay que distinguir `z = f(x1,x2)` de los ejes `x1,x2,x3`.

#### R03. Ilustración de Rosenbrock de tres variables

> ene l gif 3d me gustaria ver tambien la función ilustrada , no solo el recorrido y termina esto : **El orden que recomiendo ahora:** reparar el comando de Rastrigin; completar sus 30 corridas y estadísticas; integrar ambos problemas en los heurísticos con contadores y resultados; añadir una animación heurística; y redactar la comparación de costos y resultados.

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

## Cacería de la alucinación: verificaciones con evidencia

El enunciado permite documentar verificaciones si no se encuentran cinco
hallazgos genuinos. No disponemos aquí de cinco respuestas incorrectas literales
con evidencia suficiente para atribuirlas a la IA. Por eso los siguientes son
**controles realizados**, no cinco alucinaciones inventadas.

Las dos fichas siguientes desarrollan controles que ya aparecían en la tabla
general: representación de Rosenbrock 3D y costo equivalente de GD. Se añaden
experimentos reproducibles y resultados del 9 de octubre de 2026. **Son dos
verificaciones documentadas de la tarea de Sara, no dos respuestas erróneas
de IA demostradas.** Si se recuperan esas respuestas originales, podrán
completarse los campos de atribución sin reconstruir citas de memoria.

### V01. Distinguir Rosenbrock 3D de una superficie de Rosenbrock 2D

**Categoría:** matemáticas y representación de funciones.

1. **Prompt conservado:** R03, transcrito completo arriba. La parte pertinente
   solicita ilustrar la función en el GIF 3D, además de mostrar el recorrido.
2. **Respuesta relevante de IA:** no se conserva una respuesta literal que
   contenga un error. La afirmación que se pone a prueba —no una cita de IA—
   es que dibujar `z=f(x1,x2)` bastaría para representar Rosenbrock de tres
   variables.
3. **Motivo de la comprobación:** la altura de una superficie 2D es el valor
   de la función; la tercera coordenada de Rosenbrock 3D es otra variable de
   entrada. Confundirlas cambia el objeto matemático que se está mostrando.
4. **Evidencia:** con la implementación del proyecto,
   `f(-1.2,1)=24.2`, mientras que `f(-1.2,1,0.5)=49.2`. El término asociado
   a la tercera variable no se puede omitir. Para construir niveles reales
   de la función 3D se despeja:

   ```text
   A = 100(x2 − x1²)² + (1 − x1)² + (1 − x2)²
   x3 = x2² ± sqrt((c − A)/100), cuando A ≤ c.
   ```

   En `x1=x2=1`, los puntos con `x3=0.9` y `x3=1.1` dan `f≈1`;
   con `x3≈0.683772234` y `x3≈1.316227766` dan `f≈10`.
   El [JSON de evidencia](evidencias_ia/rosenbrock_verificaciones.json)
   conserva los valores completos. La prueba
   `test_isosurfaces_are_actual_rosenbrock_level_sets` comprueba además
   puntos de una malla para ambos niveles.
5. **Conclusión y representación correcta:** una superficie `z=f(x1,x2)`
   representa una función de dos variables. Para el GIF de Rosenbrock 3D,
   los ejes son `x1,x2,x3`, las superficies corresponden a `f=c` y el valor
   objetivo se muestra aparte. El código actual ya implementa esta
   representación; esta ficha no afirma haber encontrado y corregido ahora
   una respuesta de IA equivocada.
6. **Lección:** comprobar las variables de entrada y sustituir puntos de la
   visualización en la función original. Una gráfica atractiva no basta para
   demostrar que representa la función correcta.

### V02. Separar llamadas reales y costo equivalente del gradiente

**Categoría:** código y conceptos de comparación de costos.

1. **Prompt conservado de contexto:** R01, sobre desarrollo incremental y
   comprobación del código de Persona 1. No se conserva un prompt específico
   que pidiera la afirmación cuestionada sobre costos.
2. **Respuesta relevante de IA:** no se conserva una respuesta literal
   incorrecta. La afirmación que se contrasta —no una cita de IA— es que
   `C=N_f+2d·N_grad` corresponde al número de llamadas reales a `f` que
   realiza GD con gradiente analítico.
3. **Motivo de la comprobación:** diferencias centrales requieren dos
   evaluaciones por coordenada; una fórmula analítica de gradiente no tiene
   por qué llamar a `f`. Confundir ambas formas de cálculo atribuiría al
   optimizador evaluaciones que no ejecutó.
4. **Evidencia:** se instrumentaron las funciones con contadores de llamadas
   independientes del contador del optimizador, usando diez iteraciones y
   paso `0.001`. Los resultados se muestran en la Tabla 1.

**Tabla 1. Conteo real frente al costo equivalente de GD-Rosenbrock.**
Fuente: ejecución de `docs/evidencias_ia/verificar_rosenbrock.py`,
9 de octubre de 2026; resultados en
[rosenbrock_verificaciones.json](evidencias_ia/rosenbrock_verificaciones.json).

| Dimensión | Punto inicial | Iteraciones | Llamadas reales a f | Llamadas reales al gradiente | Costo equivalente |
|---|---|---:|---:|---:|---:|
| 2 | `(-1.2, 1.0)` | 10 | 1 | 10 | 41 |
| 3 | `(-1.2, 1.0, 0.5)` | 10 | 1 | 10 | 61 |

5. **Conclusión e interpretación correcta:** GD evalúa `f` una vez al final
   y utiliza diez evaluaciones de su gradiente analítico en estos ejemplos.
   Los valores 41 y 61 son costos equivalentes bajo la convención declarada,
   no llamadas reales a `f` ni segundos de ejecución. Las evaluaciones para
   dibujar figuras se contabilizan fuera de la optimización. El conteo actual
   es consistente; se documenta una verificación, no un defecto corregido.
6. **Lección:** instrumentar las llamadas, reportar `N_f` y `N_grad` por
   separado y explicar la equivalencia. No deducir el costo real de una
   etiqueta, del número de fotogramas ni del número de iteraciones solamente.

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

Resultado el 9 de octubre de 2026: **12 pruebas aprobadas en 4,67 s**.
Es el resultado de esta selección de pruebas; no acredita que toda la suite
del proyecto pase. Las evidencias fueron ejecutadas con asistencia del agente
y no se atribuyen automáticamente a una ejecución manual de la estudiante.

### Registro general de verificaciones de Parte 1

La siguiente tabla conserva el registro previo del equipo; V01 y V02 amplían
dos de sus controles para la parte de Sara. Las menciones a pruebas o arreglos
en este registro histórico no certifican el estado actual de todos los métodos.

| Categoría | Afirmación puesta a prueba | Evidencia y resultado | Lección |
|---|---|---|---|
| Matemáticas | El gradiente implementado corresponde a cada función. | Las pruebas de funciones contrastan derivadas analíticas con diferencias finitas en 2D/3D. Pasan en la suite. | Comprobar derivadas numéricamente además de derivarlas. |
| Matemáticas | La superficie del GIF representa Rosenbrock de tres variables. | `test_isosurfaces_are_actual_rosenbrock_level_sets` sustituye sus puntos y verifica f=1 y f=10. | En tres variables, z no debe confundirse con f; hay que indicar qué representan los ejes. |
| Código | Los contadores reflejan llamadas realmente ejecutadas. | `test_population_counts_history_and_reproducibility` instrumenta el objetivo; las pruebas de GD comprueban sus contadores separados. | Contar llamadas dentro del optimizador, no deducirlas de una gráfica. |
| Código | La visualización reproduce los datos guardados. | `test_gif_preserves_endpoints_and_saved_data` compara cada punto animado y verifica que no se alteren archivos de resultados. | Separar cálculo, persistencia y visualización. |
| Conceptos | Completar iteraciones equivale a encontrar el mínimo global. | No: GD Rastrigin principal completa corridas pero obtiene 0/30 éxitos en cada dimensión al umbral 0.0001. Ver `resultados/comparison.json`. | Separar `completed` de éxito, informar f final y umbral. |
| Conceptos | C=N_f+2dN_grad mide tiempo real. | No: es una equivalencia justificada por diferencias centrales; el código usa gradientes analíticos. Ver metodología y contadores. | Declarar la convención y no interpretarla como un cronómetro. |

En la auditoría también se encontraron parámetros inválidos aceptados por las
llamadas directas de GD (iteraciones negativas o tasa cero) y una explicación
confusa del presupuesto en el informe demo. Se agregaron validaciones y se
eliminó la referencia fija al presupuesto principal del informe generado. No
se atribuyen estos defectos a una respuesta literal de IA no conservada aquí.

Para añadir un hallazgo real, conservar: prompt literal, fragmento literal de
respuesta, sospecha, evidencia, corrección y lección. El equipo debe aportar
los hallazgos verificables de sus otras partes, si existen. No reconstruir citas
de memoria ni presentar esta tabla como cinco errores descubiertos.
