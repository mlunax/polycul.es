import sys

import polycules


if len(sys.argv) != 2:
    print('Expected ID, got too little or too much')

old_id = sys.argv[1]

db = polycules.connect_db()
result = db.execute('select hash from polycules where id = ?', [
    old_id,
]).fetchone()

if result is None:
    print("Couldn't find the polycule with that ID")

print('New url: https://polycul.es/{}'.format(result[0][:7]))
