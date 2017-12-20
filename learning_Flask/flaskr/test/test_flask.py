#!/usr/bin/env python
"""
Created on 11/16/17 2:44 PM

base Info
"""
import os
from flaskr import flask_app
import unittest
import tempfile
import flask

__author__ = 'liuchao'
__version__ = '1.0'


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, flask_app.app.config['DATABASE'] = tempfile.mkstemp()
        flask_app.app.testing = True
        self.app = flask_app.app.test_client()
        with flask_app.app.app_context():
            flask_app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask_app.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('ad', 'default')
        assert b'Invalid username' in rv.data
        rv = self.login('admin', 'de')
        assert b'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True
                           )
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

    def test_request_context(self):
        app = flask.Flask(__name__)

        with app.test_request_context('/?name=Peter'):
            assert flask.request.path == '/'
            assert flask.request.args['name'] == 'Peter'

        with app.test_client() as c:
            rv = c.get('/?id=192')
            assert flask.request.args['id'] == '192'


if __name__ == '__main__':
    unittest.main()
