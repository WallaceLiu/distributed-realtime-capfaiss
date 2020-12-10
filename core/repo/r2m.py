# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : r2m.py
@description    :


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import redis
from core.utils.udecorator import synchronized


class R2M:
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        """
        :type kwargs: object
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            _conf = kwargs
            _pool = redis.ConnectionPool(**_conf)
            cls.red = redis.Redis(connection_pool=_pool)
        return cls.instance

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        return self.red.set(key, value, ex, px, nx, xx)

    def exists(self, name):
        return self.red.exists(name)

    def get(self, name):
        return self.red.get(name)

    def set(self, name, value):
        return self.red.set(name, value)

    def hmget(self, name, keys, *args):
        return self.red.hmget(name, keys, *args)

    def hmset(self, name, mapping):
        return self.red.hmset(name, mapping)

    def hgetall(self, name):
        return self.red.hgetall(name)

    def is_exist(self, key):
        return self.red.exists(key)

    def sadd(self, name, *values):
        return self.red.sadd(name, *values)

    def smembers(self, name):
        return self.red.smembers(name)

    def srem(self, name, *values):
        return self.red.srem(name, *values)

    def delete(self, *names):
        return self.red.delete(*names)
