from six.moves import input
import sys

from model import Polycule
import polycules


db = polycules.connect_db()

id = input('Enter the ID of the polycule to delete > ')
polycule = Polycule.get(db, int(id), None, force=True)
if polycule is None:
    print('\nNo polycule with that ID found.')
    db.close()
    sys.exit(1)

if polycule.delete_pass is not None:
    confirm = input(
        '\nPolycule has a delete password, are you sure? [y/n] > ')
    if confirm[0].lower() != 'y':
        print('\nOkay, exiting without deleting.')
        db.close()
        sys.exit(1)

confirm = input(
    '\nAre you sure you want to delete {}? [y/n] > '.format(id))
if confirm[0].lower() == 'y':
    print('\nDeleting {}...'.format(id))
    polycule.delete(None, force=True)
    print('Polycule deleted.')
db.close()
