import os
import sqlite3
from flaskr.config import *
from flaskr.ListView import *
import werkzeug
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import contextmanager
from flask import appcontext_pushed, json, jsonify, Blueprint
from raven.contrib.flask import Sentry
from flask.views import View
from jinja2 import TemplateNotFound
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flaskr.models import User, UserView

app = Flask(__name__)
app.config.from_object(DebugConfig)

app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'flask.db'),
    SECRET_KEY='development key',
    # USERNAME='admin',
    # PASSWORD='default',
    # DEBUG='True',

))
app.config['DATABASE_FILE'] = 'flask.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True


app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# sentry = Sentry(app, dsn='http://127.0.0.1:5001')
admin = Admin(app, name='Flask_Admin', template_mode='bootstrap3')
admin.add_view(UserView(User, db.session, name='User'))

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()




@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


@app.route('/show_entries')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT title, text FROM entries ORDER BY id DESC ')
    entries = cur.fetchall()
    for entry in entries:
        print(entry)
    return render_template('show_entries.html', entries=entries)


def get_entries():
    db = get_db()
    cur = db.execute('SELECT title, text FROM entries ORDER BY id DESC ')
    entries = cur.fetchall()
    return entries


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('INSERT INTO entries (title, text) VALUES (?,?)', [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'][0]:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD'][0]:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    print(url_for('show_users'))
    return redirect(url_for('show_users'))


@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]


@contextmanager
def user_set(app, user):
    def handler(sender, **kwargs):
        g.user = user

    with appcontext_pushed.connected_to(handler, app):
        yield


@app.route('/users/me')
def user_me():
    return jsonify(username=g.user.username)


# with user_set(app, my_user):
#     with app.test_client() as c:
#         resp = c.get('/users/me')
#         data = json.loads(resp.data)
#         self.assert_equal(data['username'], my_user.username)

# @app.errorhandler(werkzeug.exceptions.BadRequest)
# def handle_bad_request(e):
#     return 'bad request!'
# app.register_error_handler(404, lambda e: 'bad request!')


print('app.debug')
print(app.debug)
ADMINS_MAIL = ['liuchao_mail@qq.com']

app.add_url_rule('/l/', view_func=EntryView.as_view('show_users'))
app.add_url_rule('/u/', view_func=UserAPI.as_view('u'))


if not app.debug:
    print('in error mails')
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler('127.0.0.1', 'server-error@example,com', ADMINS_MAIL, 'YourApplication Failed')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

simple_page = Blueprint('simple_page', __name__, template_folder='templates')
app.register_blueprint(simple_page)
app.register_blueprint(simple_page, url_prefix='/pages')

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show():
    # try:
    #     return render_template('pages/%s.html' % page)
    # except TemplateNotFound:
    #     abort(500)
    return 'show'


if __name__ == '__main__':

    app.run()

