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

La versión actual del proyecto utiliza distancias y duraciones estimadas **por carretera** para las 47 capitales, obtenidas mediante la matriz de **openrouteservice** (perfil `driving-car`). La consulta registrada se hizo el **13 de octubre de 2026, a las 01:05:54 UTC**, con el servicio:

`https://api.openrouteservice.org/v2/matrix/driving-car`

Las distancias se expresan en **km** y las duraciones en **horas**. El origen, el perfil, la fecha, las coordenadas consultadas y otros metadatos están documentados en `data/tsp/matrices_ors_metadata.json`.

**Esta versión ya no calcula la distancia como 1,25 veces la distancia geográfica ni el tiempo dividiendo por una velocidad fija de 95 km/h.** Esos supuestos corresponden a una etapa anterior y no deben presentarse como la metodología vigente. Las distancias y tiempos proceden de estimaciones de rutas por carretera, no de mediciones de viajes efectivamente realizados.

Las matrices que emplean los algoritmos están almacenadas localmente en `data/tsp/matrices.npz`. Se conservan para permitir ejecutar ACO y GA sin efectuar nuevamente las consultas a la API. Son estimaciones sujetas a la red vial y a los parámetros del motor de rutas en la fecha indicada; no incorporan por sí solas tarifas de peajes.

**Observación sobre archivos históricos:** `data/tsp/matrices_summary.json` todavía registra el factor 1,25, la velocidad de 95 km/h y estadísticas de la matriz anterior. Se conserva como referencia histórica, **no como descripción de las matrices actuales**. Para el origen de la matriz actual debe consultarse `matrices_ors_metadata.json`.

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

Los valores anteriores corresponden a los peajes incluidos en la matriz `tolls_eur` utilizada por el modelo de costos del proyecto. **No son tarifas oficiales verificadas para 2026**. Según `data/tsp/integration_notes.json`, la matriz de peajes proviene de la versión previa del proyecto y se considera **provisional**. Los valores cero pueden significar falta de registro; no necesariamente una carretera gratuita. La documentación disponible no confirma los importes ni la cobertura para todos los pares de ciudades. Por eso, los costos totales del TSP deben interpretarse bajo este supuesto y no como presupuestos reales certificados.

Los valores concretos de estos pares se almacenan directamente en la matriz `tolls_eur` incluida en el archivo:

`data/tsp/matrices.npz`

Esta información se conserva localmente para garantizar que la ejecución del algoritmo no dependa de conexión a internet ni de consultas externas durante la sustentación.

## 4. Datos del Vehículo y Combustible

El modelo utiliza un vehículo de referencia con un consumo homologado utilizado para estimar el costo de combustible.

Los parámetros correspondientes se encuentran almacenados en:

`data/tsp/vehicle_specs.yaml`

En el archivo constan los siguientes parámetros de referencia: **SEAT León 1.5 TSI 130 CV (manual)**, consumo WLTP de **5,4 L/100 km**, **gasolina 95** y precio de **1,58 €/L**, con fecha de consulta declarada **6 de octubre de 2026** para el combustible. Son los valores **declarados en la configuración del proyecto**; este documento no acredita una comprobación independiente de las fichas del modelo exacto ni del precio histórico del carburante.

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
- `data/tsp/matrices_ors_metadata.json`: procedencia, fecha, perfil y unidades de las matrices actuales de openrouteservice.
- `data/tsp/integration_notes.json`: integración de datos y advertencia de peajes provisionales.
- `data/tsp/matrices_summary.json`: resumen histórico de la matriz aproximada anterior; no describe las matrices viales actuales.
- `data/tsp/vehicle_specs.yaml`: parámetros del vehículo y precio del combustible.
- `data/tsp/sources_and_notes.md`: documentación metodológica y fuentes empleadas.

El almacenamiento local de estos archivos permite reproducir las ejecuciones sin realizar consultas a servicios externos.

## 6. Fuentes y trazabilidad

- **openrouteservice** (2026). Servicio de matriz de rutas `driving-car`. Endpoint: https://api.openrouteservice.org/v2/matrix/driving-car . Consulta registrada el 13 de octubre de 2026 (UTC); metadatos archivados en `matrices_ors_metadata.json`. Datos de carreteras atribuidos a OpenStreetMap y colaboradores, según metadatos de respuesta.
- **SEAT España**. Especificaciones del SEAT León. https://www.seat.es/coches/leon/especificaciones . En `vehicle_specs.yaml` se cita esta página como fuente del consumo WLTP; conviene contrastar la versión exacta del vehículo y archivar la ficha consultada.
- **Ministerio para la Transición Ecológica y el Reto Demográfico (MITECO)**. Geoportal de estaciones de servicio. https://geoportalgasolineras.es/ . En `vehicle_specs.yaml` se registra consulta del 6 de octubre de 2026 y precio de referencia de 1,58 €/L; no se adjuntó comprobante independiente del precio consultado.
- **Ministerio de Transportes y Movilidad Sostenible**. Información sobre la red vial y autopistas de peaje: https://www.transportes.gob.es/ . **No se ha verificado** que los ocho importes actualmente guardados en la matriz coincidan con tarifas oficiales vigentes.

### Limitación de uso

El modelo es útil para comparar rutas **bajo los parámetros y datos configurados**. Debido a que los peajes todavía son provisionales, no debe afirmarse que los costos calculados sean tarifas de desplazamiento exactas ni que todos los tramos sin peaje registrado sean gratuitos.
