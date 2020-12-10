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


class R2MP:
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

    def pbset(self, l, cnt):
        """

        :param l: list [(key,value),(key,value),...]
        :param cnt:
        :return:
        """
        b = int(len(l) / cnt)
        for i in range(b):
            self.pset(l[i * cnt:(i + 1) * cnt])

    def pset(self, hm):
        with self.red.pipeline(transaction=False) as p:
            for d in hm:
                p.set(d[0], d[1])
            result = p.execute()
        return result

    def pbhmset(self, l, cnt):
        """

        :param l: list [(key,value),(key,value),...]
        :param cnt:
        :return:
        """
        b = int(len(l) / cnt)
        if b == 0:
            self.phmset(l)
        else:
            for i in range(b):
                self.phmset(l[i * cnt:(i + 1) * cnt])

    def phmset(self, hm):
        with self.red.pipeline(transaction=False) as p:
            for d in hm:
                p.hmset(d[0], d[1])
            result = p.execute()
        return result

    def pget(self, keys):
        """

        :param keys: list
        :return:
        """
        with self.red.pipeline(transaction=False) as p:
            for key in keys:
                p.get(key)
            result = p.execute()
        return result

    def phgetall(self, keys):
        """

        :param keys: list
        :return:
        """
        with self.red.pipeline(transaction=False) as p:
            for key in keys:
                p.hgetall(key)
            result = p.execute()
        return result

    def phmget(self, names, key):
        """

        :param names: list name list
        :param keys: val
        :return:
        """
        with self.red.pipeline(transaction=False) as p:
            for name in names:
                p.hmget(name, key)
            result = p.execute()
        return result

    def pexists(self, keys):
        """

        :param keys:
        :return:
        """
        with self.red.pipeline(transaction=False) as p:
            for key in keys:
                p.exists(key)
            result = p.execute()
        return result

    def is_pexist(self, keys):
        if len(keys) > 0:
            with self.red.pipeline(transaction=False) as p:
                for key in keys:
                    p.exists(key)
                result = p.execute()
            return result
        else:
            return [False]

    def psmembers(self, keys):
        """

        :param keys:
        :return:
        """
        with self.red.pipeline(transaction=False) as p:
            for key in keys:
                p.smembers(key)
            result = p.execute()
        return result

    def smembers(self, key):
        """

        :param key:
        :return:
        """
        return self.red.smembers(key)

    def lock(self, name, value, time_out):
        s = self.red.setnx(name, value)
        if s == 1:
            self.red.expire(name, time_out)
        return s

    def srem(self, name, *values):
        return self.red.srem(name, *values)

    def sadd(self, name, *values):
        return self.red.sadd(name, *values)

    def delete(self, *names):
        return self.red.delete(*names)
