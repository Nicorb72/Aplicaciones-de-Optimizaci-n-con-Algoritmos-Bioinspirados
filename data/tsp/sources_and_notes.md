# Documentación de Datos y Fuentes del TSP (España Peninsular - 47 Capitales)

## 1. Definición del Problema y Capitales

Se consideran las **47 capitales de provincia de la España peninsular**.

Se excluyen por directriz del enunciado:

- Palma (Islas Baleares) — insular.
- Las Palmas de Gran Canaria y Santa Cruz de Tenerife (Canarias) — insulares.
- Ceuta y Melilla — no son provincias ni accesibles por carretera desde la península.

Total de ciudades a visitar: **47 capitales**.

El recorrido es cerrado, por lo que después de visitar todas las ciudades se regresa a la ciudad de inicio.

## 2. Modelo de Costo

Para cada par de ciudades \(i\) y \(j\), el costo de desplazamiento se calcula mediante:

\[
C_{ij}
=
(\text{valor\_hora}\times T_{ij})
+
P_{ij}
+
C_{\text{combustible},ij}
\]

donde:

- \(T_{ij}\): tiempo estimado de viaje entre las ciudades \(i\) y \(j\), en horas.
- \(P_{ij}\): costo de peajes entre las ciudades \(i\) y \(j\), en euros.
- \(D_{ij}\): distancia estimada entre las ciudades \(i\) y \(j\), en kilómetros.
- \(C_{\text{combustible},ij}\): costo estimado de combustible para desplazarse entre ambas ciudades.

El costo de combustible se calcula como:

\[
C_{\text{combustible},ij}
=
\frac{\text{consumo\_WLTP}}{100}
\times
D_{ij}
\times
\text{precio\_combustible}
\]

Por tanto, la función objetivo considera simultáneamente el costo asociado al tiempo del vendedor, el combustible utilizado y los peajes del recorrido.

### Construcción de las matrices de distancia y tiempo

Las distancias entre las 47 capitales se estimaron a partir de sus coordenadas geográficas.

Para aproximar la diferencia entre la distancia geográfica directa y un recorrido por carretera, se aplicó un factor vial de 1.25:

\[
D_{ij}
=
1.25\,D_{ij}^{geo}
\]

donde \(D_{ij}^{geo}\) representa la distancia geográfica entre las ciudades \(i\) y \(j\).

A partir de la distancia estimada se calculó el tiempo de viaje suponiendo una velocidad media de 95 km/h:

\[
T_{ij}
=
\frac{D_{ij}}{95}
\]

De esta manera, las matrices utilizadas en el modelo representan una aproximación homogénea de las distancias y los tiempos de desplazamiento entre las ciudades.

Estas matrices no corresponden a rutas obtenidas directamente de un servicio de navegación o de una API de rutas. El uso del factor vial y de una velocidad media permite mantener el conjunto de datos completamente disponible de forma local y reproducible durante la ejecución del proyecto.

Los parámetros utilizados para la construcción de las matrices son:

- Número de ciudades: 47.
- Factor vial: 1.25.
- Velocidad media utilizada: 95 km/h.
- Distancia mínima registrada en la matriz: 53.6 km.
- Distancia máxima registrada en la matriz: 1238.0 km.
- Distancia media entre pares de ciudades: aproximadamente 521.90 km.

## 3. Estado de la Red de Autopistas de Peaje en España

Durante la construcción de la matriz de peajes se tuvo en cuenta que varias autopistas españolas que históricamente fueron de pago actualmente se encuentran liberadas.

Este aspecto es relevante porque el uso de información desactualizada podría introducir costos de peaje en trayectos que actualmente son gratuitos.

### Autopistas liberadas consideradas

Entre las principales autopistas que dejaron de ser de peaje se encuentran:

- **AP-1** (Burgos - Armiñón): liberada en diciembre de 2018.
- **AP-4** (Sevilla - Cádiz): liberada en enero de 2020.
- **AP-7** (Tarragona - Valencia - Alicante): liberada en enero de 2020.
- **AP-2** (Zaragoza - Mediterráneo): liberada en agosto de 2021.
- **AP-7** (La Jonquera - Barcelona - Tarragona): liberada en agosto de 2021.

### Tramos de peaje considerados en la matriz

Se identificaron tramos de peaje todavía relevantes en los siguientes corredores:

- **AP-68**: conexión Bilbao - Logroño - Zaragoza.
- **AP-6 / AP-51 / AP-61**: conexiones de Madrid con Segovia y Ávila mediante el entorno de Guadarrama.
- **AP-66**: conexión entre León y Asturias mediante el corredor del Huerna.
- **AP-9**: autopista del Atlántico en Galicia.

La matriz utilizada en el proyecto contiene actualmente **8 pares de ciudades con valores de peaje distintos de cero**.

### Pares con peaje almacenados en la matriz

La matriz `tolls_eur` contiene valores de peaje distintos de cero para los siguientes pares de ciudades:

| Origen | Destino | Peaje almacenado (€) |
|---|---|---:|
| A Coruña | Ourense | 7.00 |
| A Coruña | Pontevedra | 18.20 |
| Ávila | Madrid | 12.50 |
| Bilbao | Logroño | 15.50 |
| Bilbao | Zaragoza | 33.50 |
| León | Oviedo | 14.30 |
| Logroño | Zaragoza | 18.00 |
| Madrid | Segovia | 7.50 |

Los valores anteriores corresponden a los peajes incluidos en la matriz `tolls_eur` utilizada por el modelo de costos del proyecto.

Los valores concretos de estos pares se almacenan directamente en la matriz `tolls_eur` incluida en el archivo:

`data/tsp/matrices.npz`

Esta información se conserva localmente para garantizar que la ejecución del algoritmo no dependa de conexión a internet ni de consultas externas durante la sustentación.

## 4. Datos del Vehículo y Combustible

El modelo utiliza un vehículo de referencia con un consumo homologado utilizado para estimar el costo de combustible.

Los parámetros correspondientes se encuentran almacenados en:

`data/tsp/vehicle_specs.yaml`

El consumo y el precio del combustible no se encuentran duplicados dentro del algoritmo de optimización. Tanto la matriz de costos como el desglose final del recorrido leen estos parámetros desde el mismo archivo de configuración.

Esto permite mantener una única fuente de información y evita inconsistencias entre el costo utilizado durante la optimización y el costo reportado al final.

La expresión utilizada para el costo de combustible es:

\[
C_{\text{combustible},ij}
=
\frac{c}{100}
D_{ij}
p
\]

donde:

- \(c\): consumo del vehículo en L/100 km.
- \(D_{ij}\): distancia estimada entre las ciudades \(i\) y \(j\).
- \(p\): precio del combustible en €/L.

## 5. Archivos de Datos Utilizados

Los datos necesarios para ejecutar el TSP se encuentran almacenados dentro del repositorio:

- `data/tsp/spain_capitals.csv`: información de las 47 capitales y sus coordenadas.
- `data/tsp/matrices.npz`: matrices de distancia, tiempo y peajes.
- `data/tsp/matrices_summary.json`: resumen de los parámetros utilizados para construir las matrices.
- `data/tsp/vehicle_specs.yaml`: parámetros del vehículo y precio del combustible.
- `data/tsp/sources_and_notes.md`: documentación metodológica y fuentes empleadas.

El almacenamiento local de estos archivos permite reproducir las ejecuciones sin realizar consultas a servicios externos.

## 6. Fuentes Citadas

Ministerio de Transportes y Movilidad Sostenible. (2024). *Mapa oficial de carreteras y autopistas de peaje del Estado*. Gobierno de España. https://www.transportes.gob.es/

Ministerio para la Transición Ecológica y el Reto Demográfico. (2026). *Geoportal de estaciones de servicio: precios de carburantes*. Gobierno de España. https://geoportalgasolineras.es/

SEAT S.A. (2024). *Manual y especificaciones técnicas: SEAT León 1.5 TSI*. SEAT España. https://www.seat.es/

Instituto Geográfico Nacional. (2024). *Nomenclátor Geográfico Básico de España*. Ministerio de Transportes y Movilidad Sostenible.