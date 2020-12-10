# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : cache_man.py
@description    : local_cache


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import logging
import os
from core.model.ufunc import *


class IdMapper(object):
    SIZE = 5

    def __init__(self):
        self.mapper = {}
        self.dt = None

    def set(self, mapper):
        self.mapper = mapper

    def get(self):
        return self.mapper


def create_item_id_mapper_hashmap(item_id_mapper_path, model, dt):
    data_hash = []
    if os.path.exists(item_id_mapper_path):
        with open(item_id_mapper_path, 'r') as f:
            l = f.readlines()
            for r in l:
                rs = r.split(',')
                key = \
                    create_item_r2m_key_by_item_and_model_name(model.config['r2m']['item'],
                                                               rs[0],
                                                               model.model_name_no_dt)
                data_hash.append((key, {'item_id': rs[1].replace('\n', ''), 'dt': dt}))
    return data_hash
