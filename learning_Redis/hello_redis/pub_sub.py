#!/usr/bin/env python
"""
Created on 12/6/17 11:22 AM

base Info
"""
import threading
import time
import redis

__author__ = 'liuchao'
__version__ = '1.0'

conn = redis.Redis()


def publisher(n):
    time.sleep(3)
    for i in range(n):
        conn.publish('channel', i)
        time.sleep(1)


def run_pubsub():
    threading.Thread(target=publisher,args=(5,)).start()
    pubsub = conn.pubsub()
    pubsub.subscribe(['channel','channel1'])
    count = 0
    for item in pubsub.listen():
        print(item)
        count += 1
        if count == 4:
            pubsub.unsubscribe(['channel'])
        # if count == 5:
        #     break


if __name__ == '__main__':
    run_pubsub()
