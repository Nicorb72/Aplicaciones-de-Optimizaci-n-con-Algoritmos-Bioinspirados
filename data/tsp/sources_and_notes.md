# Documentación de Datos y Fuentes del TSP (España Peninsular - 47 Capitales)

## 1. Definición del Problema y Capitales
Se consideran las **47 capitales de provincia de la España peninsular**.
Se excluyen por directriz del enunciado:
- Palma (Islas Baleares) — insular.
- Las Palmas de Gran Canaria y Santa Cruz de Tenerife (Canarias) — insulares.
- Ceuta y Melilla — no son provincias ni accesibles por carretera desde la península.

Total de ciudades a visitar: **47 capitales**. El recorrido es cerrado (regreso a la ciudad de inicio).

## 2. Modelo de Costo
Para cada par de ciudades $(i, j)$:
$$C_{ij} = (\text{valor\_hora} \times T_{ij}) + P_{ij} + C_{\text{combustible}, ij}$$

Donde:
- $T_{ij}$: tiempo de viaje por carretera en horas.
- $P_{ij}$: costo de peajes en euros.
- $C_{\text{combustible}, ij} = \frac{\text{consumo\_WLTP}}{100} \times D_{ij} \times \text{precio\_combustible}$.
- $D_{ij}$: distancia por carretera en kilómetros.

## 3. Estado de la Red de Autopistas de Peaje en España (Alerta de Desactualización / Cacería de Alucinación)
> **Advertencia crítica para el reporte:** Muchas bases de datos e IAs desactualizadas asumen que autopistas históricas como la AP-7 o la AP-2 siguen siendo de peaje.
- **Liberadas recientemente (gratuitas):**
  - **AP-1** (Burgos - Armiñón): liberada en diciembre de 2018.
  - **AP-4** (Sevilla - Cádiz): liberada en enero de 2020.
  - **AP-7** (Tarragona - Valencia - Alicante): liberada en enero de 2020.
  - **AP-2** (Zaragoza - Mediterráneo): liberada en agosto de 2021.
  - **AP-7** (La Jonquera - Barcelona - Tarragona): liberada en agosto de 2021.
- **Tramos con peaje remanente (incluidos en la matriz):**
  - **AP-68** (Bilbao - Logroño - Zaragoza).
  - **AP-6 / AP-51 / AP-61** (Túneles de Guadarrama: conexión Madrid con Segovia y Ávila).
  - **AP-66** (Autovía Ruta de la Plata, tramo Campomanes - León / Túnel del Negrón).
  - **AP-9** (Autopista del Atlántico en Galicia: tramos A Coruña - Santiago - Pontevedra - Vigo).

## 4. Fuentes Citadas (APA 7)
1. **Ministerio de Transportes y Movilidad Sostenible.** (2024). *Mapa Oficial de Carreteras y Autopistas de Peaje del Estado*. Gobierno de España. Recuperado en octubre de 2026, de https://www.transportes.gob.es/
2. **Ministerio para la Transición Ecológica y el Reto Demográfico (MITECO).** (2026). *Geoportal de estaciones de servicio: Precios de carburantes*. Gobierno de España. Consultado el 6 de octubre de 2026, de https://geoportalgasolineras.es/
3. **SEAT S.A.** (2024). *Manual y especificaciones técnicas: SEAT León 1.5 TSI*. SEAT España. Recuperado de https://www.seat.es/
4. **Instituto Geográfico Nacional (IGN).** (2024). *Nomenclátor Geográfico Básico de España*. Ministerio de Transportes y Movilidad Sostenible.
