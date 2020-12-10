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

from config import model_man  # , cache_r2m, cache_r2mp
from core.rc import search, add, delete, reindex, meta
from core.uconstant.response_code import *
from core.utils.utils import DateEnconding


class SearchApi(Resource):

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

            status, instance = meta(model_man, rc_id)

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

            if len(ids) != len(vectors):
                return {'code': ID_VEC_LEN_INCONSISTENT, 'msg': RESPONSE_CODE[ID_VEC_LEN_INCONSISTENT],
                        'data': None}

            status, instance = meta(model_man, rc_id)

            if status != SUCCESS:
                return {'code': status, 'msg': RESPONSE_CODE[status], 'data': None}

            status, result = add(instance, ids, vectors)
            return {'code': status, 'msg': RESPONSE_CODE[status], 'data': result}
        except Exception as ex:
            logging.error('%s' % ex)
            return {'code': FAIL, 'msg': RESPONSE_CODE[FAIL], 'data': None}


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

            status, instance = meta(model_man, rc_id)

            if status != SUCCESS:
                return {'code': status, 'msg': RESPONSE_CODE[status], 'data': None}

            status, result = delete(instance, ids)
            return {'code': status, 'msg': RESPONSE_CODE[status], 'data': result}
        except Exception as ex:
            logging.error('%s' % ex)
            return {'code': FAIL, 'msg': RESPONSE_CODE[FAIL], 'data': None}


class ReindexApi(Resource):

    def post(self):
        try:
            json_data = request.get_data()
            logging.info("requesting...<%s>" % json_data)
            d = json.loads(json_data)
            rc_id = d.get('rcId')
            ids = d.get('ids')
            vectors = d.get('vectors')

            if rc_id is None or rc_id <= 0 or ids is None or vectors is None:
                return {'code': REQUEST_ERROR, 'msg': RESPONSE_CODE[REQUEST_ERROR], 'data': None}

            if len(ids) != len(vectors):
                return {'code': ID_VEC_LEN_INCONSISTENT, 'msg': RESPONSE_CODE[ID_VEC_LEN_INCONSISTENT], 'data': None}

            status, instance = meta(model_man, rc_id)

            if status != SUCCESS:
                return {'code': status, 'msg': RESPONSE_CODE[status], 'data': None}

            status, result = reindex(instance, ids, vectors)
            return {'code': status, 'msg': RESPONSE_CODE[status], 'data': result}
        except Exception as ex:
            logging.error('%s' % ex)
            return {'code': FAIL, 'msg': RESPONSE_CODE[FAIL], 'data': None}


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

            status, result = meta(model_man, rc_id, False)

            return {'code': status, 'msg': RESPONSE_CODE[status], 'data': result}
        except Exception as ex:
            logging.error('%s' % ex)
            return {'code': FAIL, 'msg': RESPONSE_CODE[FAIL], 'data': None}


class TestApi(Resource):

    def get(self):
        return {'code': SUCCESS, 'msg': RESPONSE_CODE[SUCCESS], 'data': [1, 2, 3, 4, 5]}
