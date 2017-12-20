#!/usr/bin/env python
"""
Created on 11/16/17 10:09 AM

base Info
"""
from setuptools import setup
__author__ = 'liuchao'
__version__ = '1.0'


setup(
    name='flaskr',
    packages=['flaskr'],
    include_packages_data=True,
    install_requires=[
        'flask',

    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)




