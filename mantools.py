
######################################################

import os
import json
import time
import datetime
import shutil
import multiprocessing

######################################################

def file_size(filename):
    result = None

    try:
        result = os.path.getsize(filename)

    finally:
        return result

######################################################

def file_mkdir(filename):
    result = None

    try:
        os.makedirs(filename, exist_ok=True)

        result = True
        return

    finally:
        return result

######################################################

def file_exists(filename):
    result = None

    try:
        result = os.path.exists(filename)

    finally:
        return result

######################################################

def file_remove(filename):
    result = None

    try:
        if not file_exists(filename):
            return

        if os.path.isdir(filename):
            shutil.rmtree(filename)

        else:
            os.remove(filename)

        result = True
        return

    finally:
        return result

######################################################

def file_create(filename, data, mode='wb', encoding=None):
    result = None

    try:
        with open(filename, mode=mode, encoding=encoding) as fh:
            fh.write(data)

        result = True
        return

    finally:
        if not result:
            file_remove(filename)

        return result

######################################################

def file_read(filename, mode='rb', encoding=None):
    result = None

    try:
        with open(filename, mode=mode, encoding=encoding) as fh:
            data = fh.read()

        result = data
        return

    finally:
        return result

######################################################

def reactor_reduce(dlist, handler, ps=32):
    result = None

    try:
        if len(dlist) == 0:
            return

        ios = multiprocessing.Pool(ps)

        plist = []
        for d in dlist:
            plist.append(ios.apply_async(handler, (d,)))

        ios.close()
        ios.join()

        rlist = []
        for p in plist:
            r = p.get()
            if r:
                rlist.append(r)

        result = rlist
        return

    finally:
        return result

######################################################

def jformat(*args, **kwargs):
    result = None

    try:
        if args:
            arg = args

        elif kwargs:
            arg = kwargs

        else:
            arg = ''

        result = json.dumps(arg, ensure_ascii=False, indent=True)
        return

    finally:
        return result

######################################################

def jseri(text):
    result = None

    try:
        result = json.loads(text)

    finally:
        return result

######################################################

def mkdict(**kwargs):
    return kwargs

######################################################

def stof(s, falied=float(0)):
    result = None
    try:
        result = float(s)

    finally:
        if not result:
            return falied

        return result

######################################################

def sftime(fm='%Y-%m-%d %H:%M:%S'):
    return time.strftime(fm)

######################################################

class TimeDeltaer:
    def __init__(self):
        self.old = datetime.datetime(1979, 1, 1)
        self.new = datetime.datetime.now()

    def check(self, **kwargs):
        self.new = datetime.datetime.now()
        if self.new - self.old < datetime.timedelta(**kwargs):
            return False

        self.old = self.new
        return True

######################################################
