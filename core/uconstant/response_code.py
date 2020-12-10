# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : response_code.py
@description    : response code


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""
SUCCESS = 200
FAIL = 300
TIME_OUT = 301
INDEX_NO_EXIST = 302
REQUEST_ERROR = 303
VECTOR_EMPTY = 304
ID_LEN_ERROR = 305
ID_VEC_LEN_INCONSISTENT = 306
SYNC_ADD_MASTER_ERROR = 307
SYNC_DEL_MASTER_ERROR = 308
SYNC_REINDEX_MASTER_ERROR = 309

RESPONSE_CODE = {
    SUCCESS: 'SUCCESS',
    FAIL: 'FAIL',
    TIME_OUT: 'TIME_OUT',
    INDEX_NO_EXIST: 'INDEX_NO_EXIST',
    REQUEST_ERROR: 'REQUEST_ERROR',
    VECTOR_EMPTY: 'VECTOR_EMPTY',
    ID_LEN_ERROR: 'ID_LEN_ERROR',
    ID_VEC_LEN_INCONSISTENT: 'ID_VECTORS_LEN_INCONSISTENT',
    SYNC_ADD_MASTER_ERROR: 'SYNC_ADD_MASTER_ERROR',
    SYNC_DEL_MASTER_ERROR: 'SYNC_DEL_MASTER_ERROR',
    SYNC_REINDEX_MASTER_ERROR: 'SYNC_REINDEX_MASTER_ERROR',
}
