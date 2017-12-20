#!/usr/bin/env python
"""
Created on 12/12/17 12:56 PM

base Info
"""
from invoke import task

__author__ = 'liuchao'
__version__ = '1.0'


@task
def build(clean=False):
    # ctx.run("sphinx-build docs docs/_build")
    if clean:
        print('cleaning!')
    print('building!')


@task(help={'name':'Name of the person to say hi to.'})
def hi(name):
    """
    Say hi to someone
    :param name:
    :return:
    """
    print('Hi {}'.format(name))


