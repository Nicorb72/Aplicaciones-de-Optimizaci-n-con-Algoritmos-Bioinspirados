# Mapa de fondo del TSP

`iberia_boundaries.geojson` contiene la España peninsular y los países vecinos
visibles en el encuadre. Los límites proceden de Natural Earth, Admin 0 Countries,
escala 1:50m, en coordenadas WGS84 (longitud y latitud).

Fuente: https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/

Descarga original y hash SHA-256: `map_source.json`.

Licencia: dominio público, https://www.naturalearthdata.com/about/terms-of-use/

Se guardan los datos en el repositorio para que las gráficas y los GIF funcionen
sin internet y sin instalar bibliotecas geográficas adicionales. El fondo aparece
en `visualization/plot_tsp.py` para ACO y GA.

Las líneas azules conectan las capitales en orden de visita; no muestran la
geometría de las carreteras. Las distancias y tiempos usados por el optimizador
siguen siendo los de las matrices de OpenRouteService.
