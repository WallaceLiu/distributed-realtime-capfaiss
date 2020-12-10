# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : recall_102002_api.py
@description    :  Restful API


    ##########################################################
    #
    # Decide which model to use
    #
    #
    ##########################################################


"""

import json
import logging

from flask import request
from flask_restful import Resource

from config import model_man, context  # , cache_r2m, cache_r2mp
from core.rc import search, meta as rc_meta
from core.rc_rpc import add, delete, reindex, meta
from core.uconstant.response_code import *
from core.utils.udecorator import elapsed_time


def _get_ha():
    return context.contain['ha']


class SearchApi(Resource):

    @elapsed_time
    def post(self):
        try:
            json_data = request.get_data()
            d = json.loads(json_data)
            rc_id = d.get('rcId')
            id = d.get('id')
            vectors = d.get('vectors')
            k = d.get('k')

            if rc_id is None or vectors is None:
                return {'code': REQUEST_ERROR, 'msg': RESPONSE_CODE[REQUEST_ERROR], 'data': None}

            status, instance = rc_meta(model_man, rc_id)

            logging.info('SearchApi...%s,%s', status, instance)

            if status != SUCCESS:
                return {'code': status, 'msg': RESPONSE_CODE[status], 'data': None}

            status, d, i = search(instance, vectors, k)
            return {'code': status, 'msg': RESPONSE_CODE[status],
                    'data': [str(i).replace("'", "\""), str(d).replace("'", "\"")]}
        except Exception as ex:
            logging.error('%s' % ex)
            return {'code': FAIL, 'msg': RESPONSE_CODE[FAIL], 'data': None}


class AddApi(Resource):

    def post(self):
        try:
            json_data = request.get_data()
            d = json.loads(json_data)
            rc_id = d.get('rcId')
            ids = d.get('ids')
            vectors = d.get('vectors')

            if rc_id is None or vectors is None or ids is None:
                return {'code': REQUEST_ERROR, 'msg': RESPONSE_CODE[REQUEST_ERROR], 'data': None}

            # if len(ids) != len(vectors):
            #     return {'code': ID_VEC_LEN_INCONSISTENT, 'msg': RESPONSE_CODE[ID_VEC_LEN_INCONSISTENT],
            #             'data': None}

            ha = _get_ha()

            return add(ha, rc_id, ids, vectors)
        except Exception as ex:
            logging.error('%s' % ex)
            return {'code': FAIL, 'msg': str(ex), 'data': None}


class DelApi(Resource):

    def post(self):
        try:
            json_data = request.get_data()
            d = json.loads(json_data)
            rc_id = d.get('rcId')
            ids = d.get('ids')

            if rc_id is None or ids is None:
                return {'code': REQUEST_ERROR, 'msg': RESPONSE_CODE[REQUEST_ERROR], 'data': None}

            if len(ids) <= 0:
                return {'code': ID_LEN_ERROR, 'msg': RESPONSE_CODE[ID_LEN_ERROR],
                        'data': None}

            ha = _get_ha()

            return delete(ha, rc_id, ids)
        except Exception as ex:
            logging.error('%s' % ex)
            return {'code': FAIL, 'msg': RESPONSE_CODE[FAIL], 'data': None}


class ReindexApi(Resource):

    def post(self):
        try:
            json_data = request.get_data()
            d = json.loads(json_data)
            rc_id = d.get('rcId')
            ids = d.get('ids')
            vectors = d.get('vectors')

            if rc_id is None or ids is None or vectors is None:
                return {'code': REQUEST_ERROR, 'msg': RESPONSE_CODE[REQUEST_ERROR], 'data': None}

            if len(ids) != len(vectors):
                return {'code': ID_VEC_LEN_INCONSISTENT, 'msg': RESPONSE_CODE[ID_VEC_LEN_INCONSISTENT], 'data': None}

            ha = _get_ha()
            return reindex(ha, rc_id, ids, vectors)
        except Exception as ex:
            logging.error('%s' % ex)
            return {'code': FAIL, 'msg': str(ex), 'data': None}


class MetaApi(Resource):
    def get(self):
        try:
            json_data = request.get_data()

            if len(json_data) <= 0:
                return {'code': REQUEST_ERROR, 'msg': RESPONSE_CODE[REQUEST_ERROR], 'data': None}

            d = json.loads(json_data)
            rc_id = d.get('rcId')

            if rc_id is None:
                return {'code': REQUEST_ERROR, 'msg': RESPONSE_CODE[REQUEST_ERROR], 'data': None}

            ha = _get_ha()
            status, result = meta(ha, rc_id)

            return {'code': status, 'msg': RESPONSE_CODE[status], 'data': result}
        except Exception as ex:
            logging.error('%s' % ex)
            return {'code': FAIL, 'msg': RESPONSE_CODE[FAIL], 'data': None}


class TestApi(Resource):

    def get(self):
        return {'code': SUCCESS, 'msg': RESPONSE_CODE[SUCCESS], 'data': [1, 2, 3, 4, 5]}
