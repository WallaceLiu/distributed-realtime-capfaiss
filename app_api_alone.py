# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : app_api_alone.py
@description    : sim api


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import sys

sys.path.append('core.zip')

import os
import logging
from flask import Flask
from flask_restful import Api
from config import *
from rc_api_alone import SearchApi, ReindexApi, MetaApi, TestApi, AddApi, DelApi
from core.api.urls import urls
from core.utils.utils import load_yaml
from core.sche.uschedule import scheduler_start

# log config
logger = logging.getLogger(__name__)
logging_config = load_yaml('./logging.yml')
logging.config.dictConfig(logging_config)
logger = logging.getLogger()
#
# try:
#     scheduler = scheduler_start(context)  # cache_r2mp, cache_local, APP_UUID
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()

app = Flask(__name__)
api = Api(app)

api.add_resource(SearchApi, urls['search'])
api.add_resource(ReindexApi, urls['reindex'])
api.add_resource(AddApi, urls['add'])
api.add_resource(DelApi, urls['delete'])
api.add_resource(MetaApi, urls['meta'])
api.add_resource(TestApi, urls['test'])

if __name__ == "__main__":
    try:
        app.run(host=context.host, port=context.port)
    except (KeyboardInterrupt, SystemExit):
        # scheduler.shutdown()
        pass
