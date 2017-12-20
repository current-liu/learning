#!/usr/bin/env python
"""
Created on 11/19/17 12:58 AM

base Info

"""
from flask.views import View, MethodView
from flask import render_template

from flaskr import flask_app
from .flask_app import *

__author__ = 'liuchao'
__version__ = '1.0'


class ListView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def get_objects(self):
        raise NotImplementedError

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = {'objects': self.get_objects()}
        return self.render_template(context)


class EntryView(ListView):
    def get_template_name(self):
        return 'show_entries.html'

    def get_objects(self):
        return flask_app.get_entries()


class UserAPI(MethodView):
    """execute a different function for each HTTP
method"""

    def get(self):
        return "get"

    def post(self):
        return "post"
