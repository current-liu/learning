#!/usr/bin/env python
"""
Created on 12/6/17 2:58 PM

base Info
"""
import os
import redis
__author__ = 'liuchao'
__version__ = '1.0'


def process_logs(conn,path,callback):
    current_file, offset = conn.mget('progress:file','progress:position')
    pipe = conn.pipeline()

    def update_progress():
        pipe.mset({
            'progress:file': fname,
            'progress:position':offset
        })
        pipe.execute()

    for fname in sorted(os.listdir(path)):
        if fname < current_file:
            continue

        inp = open(os.path.join(path,fname), 'rb')
        if fname == current_file:
            inp.seek(int(offset, 10))
        else:
            offset = 0

        current_file = None

        for lno, line in enumerate(inp):
            callback(pipe, line)
            offset += int(offset) + len(line)

            if not  (lno + 1) % 1000:
                update_progress()
        update_progress()

        inp.close()




