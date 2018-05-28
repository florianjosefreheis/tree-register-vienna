import requests
import json
import sqlite3

conn = sqlite3.connect('tree_register_vienna.sqlite', timeout=10)
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Tree;

CREATE TABLE Tree (
    id                  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    dataset_id          TEXT UNIQUE,
    longitude           INTEGER,
    latitude            INTEGER,
    district            TEXT,
    street              TEXT, 
    area                TEXT, 
    tree_species        TEXT, 
    year_of_planting    INTEGER, 
    trunk_circumference INTEGER, 
    high                INTEGER, 
    high_str            TEXT, 
    crown               INTEGER, 
    crown_str           TEXT 
)
''')

# Read dataset
json_file = 'BAUMKATOGD.json'

str_data = open(json_file).read()
json_data = json.loads(str_data)
trees = json_data['features']
avg = len(trees) / 414.6 

print('There are ' + str(round(avg)) + ' trees per km² in Vienna!')

counter = 0
for tree in trees:
    dataset_id = tree['id']
    longitude = tree['geometry']['coordinates'][0]
    latitude = tree['geometry']['coordinates'][1]
    district = tree['properties']['BEZIRK']
    street = tree['properties']['OBJEKT_STRASSE']
    area = tree['properties']['GEBIETSGRUPPE']
    tree_species = tree['properties']['GATTUNG_ART']
    year_of_planting = tree['properties']['PFLANZJAHR']
    trunk_circumference = tree['properties']['STAMMUMFANG']
    high = tree['properties']['BAUMHOEHE']
    high_str = tree['properties']['BAUMHOEHE_TXT']
    crown = tree['properties']['KRONENDURCHMESSER']
    crown_str = tree['properties']['KRONENDURCHMESSER_TXT']
    
    if "'" in street:
        street = street.replace("'", "")
    
    cur.execute('''INSERT OR IGNORE INTO Tree (dataset_id, longitude,
                                               latitude, district,
                                               street, area, tree_species,
                                               year_of_planting, trunk_circumference, high,
                                               high_str, crown, crown_str)
                    VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,? )''',
                    ( dataset_id, longitude, latitude, district, street, area,
                     tree_species, year_of_planting, trunk_circumference, high,
                     high_str, crown, crown_str) )
    conn.commit()
    
    counter += 1
    print((counter, dataset_id, longitude, latitude, district))



