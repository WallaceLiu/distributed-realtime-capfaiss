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
from cacheout import CacheManager, LFUCache
from core.utils.udecorator import synchronized
import logging


class Cache(object):
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        logging.info('init cache management...')
        self.cache = CacheManager(kwargs, cache_class=LFUCache)

    def get(self, key):
        return self.cache[key]
