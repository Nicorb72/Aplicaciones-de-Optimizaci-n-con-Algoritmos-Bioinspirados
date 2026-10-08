# Uso de IA y Cacería de la alucinación — Parte 1

Este registro describe la asistencia de IA en esta conversación. El equipo debe
complementarlo con sus otras conversaciones y revisar las afirmaciones antes
de incorporarlo al blog. No acredita que cada integrante haya escrito todo el
código sin ayuda ni sustituye la explicación individual en la sustentación.

## Prompts conservados e impacto

Los siguientes prompts son literales de la conversación de Sara:

> Bien. Ahora implementemos únicamente el primer cambio necesario para Persona 1. Haz el cambio mínimo posible, explícame antes qué vas a modificar y después explícame línea por línea lo nuevo. No avances al siguiente requisito hasta comprobar que este funciona.

Impacto: desarrollo incremental de Rosenbrock y GD, con explicaciones y pruebas.
La responsabilidad de comprender y defender el código sigue siendo del equipo.

> se ve un poco generico, haslo mas girly y solo se necesita animaciṕn en 2d?

Impacto: adaptación visual de las animaciones a una paleta rosa y lavanda.
La estética no cambia las trayectorias guardadas ni los contadores del algoritmo.
El enunciado pide animar GD y al menos un heurístico; no exige expresamente un
GIF separado para cada dimensión. El proyecto incluye también GD 3D.

> ene l gif 3d me gustaria ver tambien la función ilustrada , no solo el recorrido y termina esto : **El orden que recomiendo ahora:** reparar el comando de Rastrigin; completar sus 30 corridas y estadísticas; integrar ambos problemas en los heurísticos con contadores y resultados; añadir una animación heurística; y redactar la comparación de costos y resultados.

Impacto: integración de ambos problemas, informe comparativo y superficies de
nivel en Rosenbrock 3D. Las ecuaciones y las pruebas deben consultarse junto al
código; una figura agradable no demuestra por sí sola que sea correcta.

## Cacería de la alucinación: verificaciones con evidencia

El enunciado permite documentar verificaciones si no se encuentran cinco
hallazgos genuinos. No disponemos aquí de cinco respuestas incorrectas literales
con evidencia suficiente para atribuirlas a la IA. Por eso los siguientes son
**controles realizados**, no cinco alucinaciones inventadas.

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
