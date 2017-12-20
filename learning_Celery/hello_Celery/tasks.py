#!/usr/bin/env python
"""
Created on 12/7/17 9:43 PM

base Info
"""
import time
from celery import Celery

__author__ = 'liuchao'
__version__ = '1.0'

celery_app = Celery('tasks', backend='redis://localhost:6379', broker='redis://localhost:6379')


@celery_app.task
def add(x, y):
    return x + y


@celery_app.task
def mul(x, y):
    return x * y


@celery_app.task
def xsum(numbers):
    return sum(numbers)
