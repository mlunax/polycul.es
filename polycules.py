import base64
import os
import sqlite3
from contextlib import closing

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
)

from model import Polycule

# Config
DATABASE = 'dev.db'
DEBUG = True
SECRET_KEY = 'development key'

# App initialization
app = Flask(__name__)
app.config.from_object(__name__)


# Database initialization
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def migrate():
    migrations_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'migrations')
    with closing(connect_db()) as db:
        for filename in os.listdir(migrations_dir):
            with open(os.path.join(migrations_dir, filename), 'rb') as f:
                db.cursor().execute(f.read())


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = base64.b64encode(os.urandom(12))
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token


@app.before_request
def before_request():
    if request.method == 'POST':
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return render_template('error.jinja2', error='Token expired :(')
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# Views
@app.route('/')
def front():
    """ Render the front page. """
    return render_template('front.jinja2')


@app.route('/<int:polycule_id>', methods=['GET', 'POST'])
def view_polycule(polycule_id):
    """ View a polycule. """
    try:
        polycule = Polycule.get(g.db, polycule_id,
                                request.form.get('view_pass', b''))
    except Polycule.PermissionDenied:
        return render_template('view_auth.jinja2')
    if polycule is None:
        return render_template('error.jinja2', error='Polycule not found :(')
    return render_template('view_polycule.jinja2', polycule=polycule)


@app.route('/embed/<int:polycule_id>')
def embed_polycule(polycule_id):
    """ View just a polycule for embedding in an iframe. """
    polycule = Polycule.get(g.db, polycule_id, request.form.get('view_pass'))
    if polycule is None:
        return render_template('error.jinja2', error='Polycule not found :(')
    return render_template('embed_polycule.jinja2', graph=polycule.graph)


@app.route('/inherit/<int:polycule_id>', methods=['GET', 'POST'])
def inherit_polycule(polycule_id):
    """
    Take a given polycule and enter create mode, with that polycule's contents
    already in place
    """
    try:
        polycule = Polycule.get(g.db, polycule_id,
                                request.form.get('view_pass', b''))
    except Polycule.PermissionDenied:
        return render_template('view_auth.jinja2')
    if polycule is None:
        return render_template('error.jinja2', error='Polycule not found :(')
    return render_template('create_polycule.jinja2', inherited=polycule.graph)


@app.route('/create')
def create_polycule():
    """ Create a new, blank polycule. """
    graph = """{
        "lastId": 0,
        "nodes": [],
        "links": []
    }"""
    return render_template('create_polycule.jinja2', inherited=graph)


@app.route('/save', methods=['POST'])
def save_polycule():
    """ Save a created polycule. """
    # TODO check json encoding, check size
    try:
        polycule = Polycule.create(
            g.db,
            request.form['graph'],
            request.form.get('view_pass', b''),
            request.form.get('delete_pass', b''))
    except Polycule.IdenticalGraph:
        return render_template('error.jinja2', error='An identical polycule '
                               'to the one you submitted already exists!')
    return redirect('/{}'.format(polycule.id))


@app.route('/delete/<int:polycule_id>', methods=['POST'])
def delete_polycule(polycule_id):
    polycule = Polycule.get(g.db, polycule_id, None, force=True)
    if polycule is None:
        return render_template('error.jinja2', error='Polycule not found :(')
    try:
        polycule.delete(request.form.get('delete_pass', b''))
    except Polycule.PermissionDenied:
        return render_template('view_auth.jinja2', polycule_id=polycule_id)
    return redirect('/')


if __name__ == '__main__':
    app.run()
