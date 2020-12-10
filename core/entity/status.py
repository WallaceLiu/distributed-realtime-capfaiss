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
import time  # 引入time模块
import json
import pickle


class Status(object):
    def __init__(self):
        self.ts = int(round(time.time() * 1000))
        self.action = None  # ADD DEL SCH RIX
        self.data_keys = []


status = Status()
print(pickle.dumps(status))
