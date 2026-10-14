from pathlib import Path
import csv
import argparse
import hashlib
import io
import json
import math
import zipfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description="Contrasta las coordenadas con una descarga de ES.zip de GeoNames.")
parser.add_argument("--archive", type=Path, required=True, help="Ruta a ES.zip descargado de GeoNames")
args = parser.parse_args()
archive = args.archive
with zipfile.ZipFile(archive) as z:
    records = [line.split('\t') for line in z.read('ES.txt').decode('utf-8').splitlines()]
cities = [r for r in records if r[6]=='P' and r[7] in {'PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC'} and int(r[14] or 0)>15000]

def distance(lat1, lon1, lat2, lon2):
    a,b,c,d = map(math.radians, (lat1, lon1, lat2, lon2))
    h = math.sin((c-a)/2)**2 + math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))

rows = []
with (ROOT/'data/tsp/spain_capitals.csv').open(encoding='utf-8') as f:
    for city in csv.DictReader(f):
        lat, lon = float(city['lat']), float(city['lon'])
        match = min(cities, key=lambda r: distance(lat,lon,float(r[4]),float(r[5])))
        delta = distance(lat,lon,float(match[4]),float(match[5]))
        assert delta < 5, (city['city'], match[1], delta)
        rows.append({'city':city['city'], 'stored_lat':lat, 'stored_lon':lon,
                     'geonames_id':int(match[0]), 'reference_name':match[1],
                     'reference_lat':float(match[4]), 'reference_lon':float(match[5]),
                     'separation_km':delta,
                     'reference_url':f'https://www.geonames.org/{match[0]}/'})
evidence = {
    'reference':'GeoNames, ES.zip; populated places with population >15000, excluding neighbourhoods',
    'source_url':'https://download.geonames.org/export/dump/ES.zip',
    'source_documentation':'https://download.geonames.org/export/dump/',
    'source_consulted_on':'2026-10-13',
    'license':'CC BY 4.0; GeoNames',
    'source_archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
    'stored_coordinates_sha256':hashlib.sha256((ROOT/'data/tsp/spain_capitals.csv').read_bytes()).hexdigest(),
    'method':'Nearest populated place >15000 residents, country ES, feature code PPL/PPLA/PPLA2/PPLA3/PPLA4/PPLC (neighbourhoods excluded); great-circle separation on a sphere R=6371.0088 km; name correspondence must be reviewed after regenerating.',
    'scope':'Independent geographic cross-check, not a claim about the historical source of the CSV. Coordinates remain unchanged; city centres can differ by source. Does not verify road snapping or tariffs.',
    'city_count':len(rows), 'max_separation_km':max(r['separation_km'] for r in rows), 'cities':rows}
(ROOT/'data/tsp/coordinates_evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for row in rows:
    print(row['city'], '->', row['reference_name'], round(row['separation_km'],3))
print('Maximum separation km:', evidence['max_separation_km'])
