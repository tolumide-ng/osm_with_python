#!usr/bin/env python3
from geopy.geocoders import Nominatim
import overpy
import requests
import json
from pprint import pprint as pp


geolocator = Nominatim(user_agent='Naija')
loc = geolocator.geocode('Nigeria')

area_id = int(loc.raw.get('osm_id')) + 3600000000

print(area_id)
overpass_url = "http://overpass-api.de/api/interpreter"
api = overpy.Overpass()
overpass_query = f"""
[out:json];
area({area_id})->.searchArea;
(node["amenity"="atm"](area.searchArea);
 node["amenity"="bank"](area.searchArea);
 way["amenity"="atm"](area.searchArea);
 way["amenity"="bank"](area.searchArea);
 relation["amenity"="atm"](area.searchArea);
 relation["amenity"="bank"](area.searchArea);
);
out center;
"""

print(overpass_query)

response = requests.get(overpass_url,
                        params={'data': overpass_query})

val = response.json()
banks = val['elements']

atms_true = []
all_result = []
for val in banks:
    all_result.append(val)
    if 'atm' in val['tags']:
        atms_true.append(val)


try:
    with open('all_results.txt', 'w', encoding='utf-8') as f:
        f.write('This file contains {} results\n'.format(len(all_result)))
        json.dump(all_result, f)
    with open('all_atms.txt', 'w', encoding='utf-8') as atm:
        atm.write(f'This file contains {len(atms_true)} results\n')
        json.dump(atms_true, atm)
except IOError as e:
    print(e)
