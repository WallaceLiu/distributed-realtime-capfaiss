# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : model_man.py
@description    : load model


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import logging
import json
from core.utils.udecorator import synchronized
from core.core.su_index import SimpleFlatIndex
from core.utils.io_utils import write


class IndexMan:
    instance = None
    holder = {}

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self._config = None

    def initialize(self, config):
        self._config = config
        logging.info('init rc indexes...', config)
        for rc_id in config.keys():
            self.add(str(rc_id), config[rc_id])
        logging.info('load model_man...%s' % str(self.holder.keys()))

    def add(self, rc_id, config):
        idx = SimpleFlatIndex(rc_id, config)
        idx.restore()
        self.holder[str(rc_id)] = idx
        logging.info("\tloading %s...true" % rc_id)

    def contain(self, rc_id):
        return rc_id in self.holder.keys()

    def get(self, rc_id):
        return self.holder[rc_id]


class IndexPersit:
    instance = None

    @synchronized
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    def persit(self, man, bl):
        for m in man.holder:
            if m.status and bl:
                m.save()

    def persit_one(self, man, rc_id):
        if rc_id in man.holder.keys():
            m = man.holder[rc_id]
            m.save()
