# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : urls.py
@description    : Restful API Urls


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
import logging

from config import context

urls = {
    "search": context.root_rc_router + '/search',
    "reindex": context.root_rc_router + '/reindex',
    "delete": context.root_rc_router + '/del',
    "add": context.root_rc_router + '/add',
    "meta": context.root_rc_router + '/meta',
    "test": context.root_rc_router + '/test',
}

logging.info('loaded web api urls router...')
for key in urls.keys():
    logging.info('loaded web api urls router...%s' % urls[key])
