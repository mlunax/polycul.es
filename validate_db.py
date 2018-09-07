# Validate every row in the database to make sure the graph is valid JSON

from jsonschema import validate
import json
import sqlite3


DATABASE = 'dev.db'


def validatejson(body):
    with open('schema.json') as json_data:
        schema = json.load(json_data)
    return validate(json.loads(body), schema)


db = sqlite3.connect(DATABASE)
for row in db.execute('SELECT graph, hash FROM polycules'):
    print(row[1], validatejson(row[0]))
