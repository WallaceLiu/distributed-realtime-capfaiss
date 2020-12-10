# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : uhbase.py
@description    :


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import happybase
from core.utils.udecorator import synchronized


class UHBase:
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        """
        :type kwargs: object
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            _conf = kwargs
            cls.conn = happybase.Connection(**_conf)
        return cls.instance

    def table(self, tablename):
        return self.conn.table(tablename)
