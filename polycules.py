import base64
import os
import sqlite3

from contextlib import closing
from flask import (
    abort,
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
)

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


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


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
            abort(403)
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


@app.route('/<int:polycule_id>')
def view_polycule(polycule_id):
    """ View a polycule. """
    cur = g.db.execute('select graph from polycules where id = ?',
        [polycule_id])
    if cur.arraysize != 1:
        abort(404)
    graph = cur.fetchone()[0]
    return render_template('view_polycule.jinja2', graph=graph, id=polycule_id)


@app.route('/embed/<int:polycule_id>')
def embed_polycule(polycule_id):
    """ View just a polycule for embedding in an iframe. """
    cur = g.db.execute('select graph from polycules where id = ?',
        [polycule_id])
    if cur.arraysize != 1:
        abort(404)
    graph = cur.fetchone()[0]
    return render_template('embed_polycule.jinja2', graph=graph)


@app.route('/inherit/<int:polycule_id>')
def inherit_polycule(polycule_id):
    """
    Take a given polycule and enter create mode, with that polycule's contents
    already in place
    """
    cur = g.db.execute('select graph from polycules where id = ?',
        [polycule_id])
    if cur.arraysize != 1:
        abort(404)
    graph = cur.fetchone()[0]
    return render_template('create_polycule.jinja2', inherited=graph)


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
    g.db.execute('insert into polycules (graph) values (?)',
        [request.form['graph']])
    g.db.commit()
    cur = g.db.execute('select id from polycules order by id desc limit 1')
    return redirect('/{}'.format(cur.fetchone()[0]))


if __name__ == '__main__':
    app.run()
