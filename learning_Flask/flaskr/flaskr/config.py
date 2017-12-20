#!/usr/bin/env python
"""
Created on 11/17/17 12:27 PM

base Info
"""
__author__ = 'liuchao'
__version__ = '1.0'


class Config(object):
    USERNAME = 'admin',
    PASSWORD = 'default',


class DebugConfig(Config):
    DEBUG = True
