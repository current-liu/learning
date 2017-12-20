#!/usr/bin/env python
"""
Created on 12/6/17 12:06 PM

base Info
"""
import threading
import time
import redis

__author__ = 'liuchao'
__version__ = '1.0'


conn = redis.Redis()
conn.set('notrans:',0)

def notrans():
    print(conn.incr('notrans:'))
    time.sleep(.1)
    # conn.incr('notrans:',-1)
    print(conn.incr('notrans:',-1))

if 1:
    for i in range(3):
        threading.Thread(target=notrans).start()
    time.sleep(.5)



def trans():
    print("in trans()")
    time.sleep(1)
    pipeline = conn.pipeline()
    pipeline.incr('trans:')
    time.sleep(.1)
    pipeline.incr('trans:',-1)
    print(pipeline.execute())

if 1:
    for i in range(3):
        threading.Thread(target=trans).start()
    time.sleep(.5)



