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
from core.utils.utils import load_yaml
from core.utils.udecorator import synchronized
import logging
from core.utils.ducc_utils import DuccClient
import json


class Config(object):
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, f):
        self._config = load_yaml(f)
        # self.__init_config__()
        self.contain = {}
        logging.info('loading app config...%s' % json.dumps(self._config, sort_keys=False, indent=2))

    def init_config(self, ducc):
        req = ducc.querys()
        data = json.loads(req.content)
        config_data = data['data']

        def __init_config_child(parent, config_data):
            for key in parent.keys():
                if type(parent[key]) is dict:
                    __init_config_child(parent[key], config_data)
                else:
                    if type(parent[key]) is str and 'ducc:' in str(parent[key]):
                        v = self._find_ducc(str(parent[key]).replace('ducc:', ''), config_data)
                        parent[key] = v

        for key in self._config.keys():
            if type(self._config[key]) is dict:
                __init_config_child(self._config[key], config_data)
            else:
                if type(self._config[key]) is str and 'ducc:' in str(self._config[key]):
                    self._config[key] = self._find_ducc(key, config_data)

    def _find_ducc(self, key, config_data):
        for d in config_data:
            if key == d['key']:
                v = d['value']
                try:
                    v = json.loads(d['value'])
                except RuntimeError as ex:
                    pass
                return v
        return None

    def get_section(self):
        return self._config

    def get_rpcConfig(self):
        return self.get_section()['rpc']

    def get_zkConfig(self):
        return self.get_section()['zk']

    def get_env(self):
        return self.get_section()['env']

    def get_app_section(self):
        return self._config['app']

    def set_contain(self, p):
        self.contain = p

    @property
    def host(self):
        return self.get_app_section()['host']

    @property
    def port(self):
        return self.get_app_section()['port']

    @property
    def root_rc_router(self):
        return self.get_app_section()['root_rc_path']

    #
    # @property
    # def root_sim_router(self):
    #     return self.get_app_section()['root_sim_path']

    def get_cache_local_section(self):
        return self._config['cache_local']

    def get_repo_section(self):
        return self._config['repo']

    def get_rc_section(self):
        return self._config['rc']

    def get_jss_section(self):
        return self._config['jss']

    @property
    def access_key(self):
        return self.get_jss_section()['access_key']

    @property
    def secret_key(self):
        return self.get_jss_section()['secret_key']
