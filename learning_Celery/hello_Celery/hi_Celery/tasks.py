#!/usr/bin/env python
"""
Created on 12/7/17 9:43 PM

base Info
"""
from celery import chain

from .celery_app import app

__author__ = 'liuchao'
__version__ = '1.0'


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    chain = mul.s(3,3)
    return sum(numbers)
