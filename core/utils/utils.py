# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : utils.py
@description    : utils


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import yaml
import os
import re
import datetime as dt
from datetime import datetime
import json
import numpy as np


class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


class YmlLoader(yaml.Loader):

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]

        super(YmlLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, YmlLoader)


YmlLoader.add_constructor('!include', YmlLoader.include)


def load_yaml(yaml_file):
    with open(yaml_file) as f:
        config = yaml.load(f, YmlLoader)  # Loader=yaml.FullLoader
    return config


def load_yaml_safe(yaml_file):
    with open(yaml_file) as f:
        config = yaml.safe_load(f)
    return config


def save(filename, content):
    with open(filename, 'w') as f:
        for c in content:
            f.write(c)


def savebyte(filename, buf):
    with open(filename, 'ba') as f:
        f.write(buf)
    f.close()


TOMORROW = str(dt.date.today() + dt.timedelta(1))
YESTERDAY = str(dt.date.today() + dt.timedelta(-1))


def get_yesterday():
    return str(dt.date.today() + dt.timedelta(-1))


DAY_BEFORE_YESTERDAY = str(dt.date.today() + dt.timedelta(-2))
TODAY = str(dt.date.today())

_dt = datetime.now().time()
# hours, minutes, seconds of day
HOURS_OF_TODAY = _dt.hour
MINUTES_OF_TODAY = (_dt.hour * 60 + _dt.minute) * 60
SECONDS_OF_TODAY = (_dt.hour * 60 + _dt.minute) * 60 + _dt.second


def fmat(dt, f='%Y-%m-%d'):
    return datetime.strptime(dt, f)


def sub(d1, d2):
    return d2 - d1


def subStr(d1_str, d2_str, f='%Y-%m-%d'):
    return sub(fmat(d1_str, f), fmat(d2_str, f))
