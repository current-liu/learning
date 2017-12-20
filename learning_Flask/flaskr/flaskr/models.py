#!/usr/bin/env python
"""
Created on 12/15/17 4:08 PM

base Info
"""
import flaskr.flask_app
from flask_sqlalchemy import SQLAlchemy
from flask_admin.form import rules
from flask_admin.contrib import sqla
__author__ = 'liuchao'
__version__ = '1.0'

db = SQLAlchemy(flaskr.flask_app.app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(64))
    last_name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(128))
    phone = db.Column(db.Unicode(32))
    city = db.Column(db.Unicode(128))
    country = db.Column(db.Unicode(128))
    notes = db.Column(db.UnicodeText)


class UserView(sqla.ModelView):
    """
    This class demonstrates the use of 'rules' for controlling the rendering of forms.
    """
    form_create_rules = [
        # Header and four fields. Email field will go above phone field.
        rules.FieldSet(('first_name', 'last_name', 'email', 'phone'), 'Personal'),
        # Separate header and few fields
        rules.Header('Location'),
        rules.Field('city'),
        # String is resolved to form field, so there's no need to explicitly use `rules.Field`
        'country',
        # Show macro from Flask-Admin lib.html (it is included with 'lib' prefix)
        rules.Container('rule_demo.wrap', rules.Field('notes'))
    ]

    # Use same rule set for edit page
    form_edit_rules = form_create_rules

    create_template = 'rule_create.html'
    edit_template = 'rule_edit.html'
