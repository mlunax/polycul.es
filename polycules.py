import base64
import os
import sqlite3

from contextlib import closing
from flask import (
    abort,
    Flask,
    request,
    session,
    g,
    redirect,
    url_for,
    abort,
    render_template,
    flash
)

DATABASE = 'dev.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    if request.method == 'POST':
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
    session['csrf_token'] = base64.b64encode(os.urandom(12))
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def front():
    """ Render the front page. """
    return render_template('front.jinja2')

@app.route('/<int:polycule_id>')
def view_polycule(polycule_id):
    """ View a polycule. """
    return render_template('view_polycule.jinja2')

@app.route('/embed/<int:polycule_id>')
def embed_polycule(polycule_id):
    """ View just a polycule for embedding in an iframe. """
    return render_template('embed_polycule.jinja2')

@app.route('/inherit/<int:polycule_id>')
def inherit_polycule(polycule_id):
    """
    Take a given polycule and enter create mode, with that polycule's contents
    already in place
    """
    return render_template('create_polycule.jinja2', inherited=None)

@app.route('/create')
def create_polycule(polycule_id):
    """ Create a new, blank polycule. """
    return render_template('create_polycule.jinja2')

@app.route('/save', methods=['POST'])
def save_polycule():
    """ Save a created polycule. """
    return redirect('/')

if __name__ == '__main__':
    app.run()
