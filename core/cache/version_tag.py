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
from queue import Queue


class VersionTag(object):
    SIZE = 5

    def __init__(self):
        self.user = Queue(self.SIZE)
        self.item = Queue(self.SIZE)

    def set(self, user, items):
        self.set_user(user)
        self.set_items(items)

    def set_user(self, u):
        if u is not None:
            self._set(self.user, u)

    def set_items(self, items):
        for item in items[:self.SIZE]:
            self._set(self.item, item)

    def set_item(self, item):
        self._set(self.item, item)

    def get_user(self):
        return self._get(self.user)

    def get_item(self):
        return self._get(self.item)

    def _set(self, q, u):
        if not q.full():
            return -1
        q.queue.append(u)

    def _get(self, q):
        return [] if q.empty() else list(q.queue)
