import hashlib


def migrate(db):
    rows = db.execute('select * from polycules')
    cur = db.cursor()
    for row in rows.fetchall():
        sha = hashlib.sha1(row[1].encode('utf-8')).hexdigest()
        cur.execute('update polycules set hash = ? where id = ?', [
            sha,
            row[0],
        ])
    db.commit()
