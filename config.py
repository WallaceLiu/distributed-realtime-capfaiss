# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : context.py
@description    : config


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import logging
import uuid

import logging.config
from core.context.conf import Config
from core.model.index_man import IndexMan
from core.utils.utils import load_yaml
from core.uconstant import response_code
from core.coordinate.HaMaster import HAMaster
from core.model.index_man import IndexPersit, IndexMan
from core.utils.ducc_utils import DuccClient

# log config
logger = logging.getLogger(__name__)
logging_config = load_yaml('./logging.yml')
logging.config.dictConfig(logging_config)
logger = logging.getLogger()

APP_NAME = 'cap-faiss'

# app context
context = Config(f='./config.yml')

ducc = DuccClient(context.get_section()['ducc'])

context.init_config(ducc)

model_man = IndexMan()
model_man.initialize(context.get_section()['rc'])

context.set_contain({
    'ha': HAMaster(context.get_zkConfig(), ducc),
    'index_persit': IndexPersit(),
    'index_man': IndexMan(),
    'model_man': model_man,
    'ducc': ducc,
})

# local cache
# cache_local = Cache(**Config().get_cache_local_section())
# cache_local.cache.clear_all()
# r2m
# cache_r2m = R2M(**Config().get_repo_section()['r2m'])
# r2mp
# cache_r2mp = R2MP(**Config().get_repo_section()['r2m'])
