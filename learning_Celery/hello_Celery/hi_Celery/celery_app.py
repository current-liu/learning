#!/usr/bin/env python
"""
Created on 12/8/17 9:59 AM

base Info
"""
from celery import Celery

__author__ = 'liuchao'
__version__ = '1.0'

app = Celery('hi_celery', broker='redis://localhost:6379', backend='redis://localhost:6379',
                    include=['hi_Celery.tasks'])

app.conf.update(
    result_expires=3600
)

if __name__ == '__main__':
    app.start()
