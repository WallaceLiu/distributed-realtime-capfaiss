# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : ducc_utils.py
@description    : ducc_utils


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import os
import requests
from core.utils.udecorator import *
import logging
import json


class DuccClient:
    instance = None
    root = 'http://'
    app = 'cap-config'
    ns = 'cap_faiss'
    token = '123456'
    cfg = 'admin'
    env = 'pre'
    item_short = '%s/namespace/%s/config/%s/profile/%s/item'
    item_long = '%s/namespace/%s/config/%s/profile/%s/item/%s'
    items = '%s/namespace/%s/config/%s/profile/%s/items'

    java_properties = """

"""

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, params):
        self.root = params['root']
        self.app = params['app']
        self.ns = params['ns']
        self.token = params['token']
        self.cfg = params['config']
        if 'env' in params:
            self.env = params['env']

    def is_exist(self, key):
        r = self.query(key)
        c = json.loads(r.content)
        if c['status'] == 404:
            return False
        else:
            return True

    def update(self, key, data):
        headers = {
            'application': self.app,
            'token': self.token,
        }
        url = self.item_long % (self.root, self.ns, self.cfg, self.env, key)
        r = requests.put(url, data=json.dumps(data), headers=headers)
        return r

    def updates(self, data):
        headers = {
            'application': self.app,
            'token': self.token,
        }
        url = self.items % (self.root, self.ns, self.cfg, self.env)
        d = self.java_properties.join(["%s=%s" % (k, data[k]) for k in data.keys()])
        r = requests.put(url, data=d, headers=headers)
        return r

    def delete(self, key):
        url = self.item_long % (self.root, self.ns, self.cfg, self.env, key)
        r = requests.delete(url)
        return r

    def add(self, data):
        headers = {
            'application': self.app,
            'token': self.token,
            'content-type': 'application/json;charset=UTF-8',
        }
        url = self.item_short % (self.root, self.ns, self.cfg, self.env)
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return r

    def adds(self, data):
        headers = {
            'application': self.app,
            'token': self.token,
        }
        url = self.items % (self.root, self.ns, self.cfg, self.env)
        d = self.java_properties.join(["%s=%s" % (k, data[k]) for k in data.keys()])
        r = requests.post(url, data=d, headers=headers)
        return r

    def query(self, key):
        headers = {
            'application': self.app,
            'token': self.token,
            'content-type': 'application/json;charset=UTF-8',
        }

        url = self.item_long % (self.root, self.ns, self.cfg, self.env, key)
        r = requests.get(url, headers=headers)
        return r

    def querys(self):
        headers = {
            'application': self.app,
            'token': self.token,
            'content-type': 'application/json;charset=UTF-8',
        }

        url = self.items % (self.root, self.ns, self.cfg, self.env)
        r = requests.get(url, headers=headers)
        return r


if __name__ == "__main__":
    import sys
    import json

    ducc = DuccClient({'root': 'http://ducc-api.jd.local/v1',
                       'app': 'cap-config',
                       'ns': 'cap_faiss',
                       'token': '123456',
                       'config': 'admin',
                       'env': 'pre', })

    req = ducc.is_exist('s')
    req = ducc.add({"key": "auto_key_2", "value": "v1543894564036", "description": "swith variable"})
    req = ducc.delete('auto_key_2')
    req = ducc.update('status', {
        "value": json.dumps({
            'ts': int(round(time.time() * 1000)),
            'action': "Add",
            'data_key': ['data_1_1'],
        }),
        "description": 'desc',
    })
    req = ducc.query('status')
    req = ducc.querys()
    req = ducc.updates({'k1': 'v11',
                        'k2': 'v22', })
    print('req', req.content)
