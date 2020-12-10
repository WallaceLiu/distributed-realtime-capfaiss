# encoding: utf-8
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@file           : recall_sku_rec_core.py
@description    : sku推荐


    ##########################################################
    #
    #
    #
    #
    ##########################################################


"""

import numpy as np

# from config import model_man  # , cache_r2m, cache_r2mp
from core.uconstant.response_code import *
from core.utils.udecorator import elapsed_time


@elapsed_time
def search(instance, vectors, k):
    if k is None or k <= 0:
        rk = int(instance.params['k'])
    else:
        rk = k

    if len(vectors) > 0:
        np_vectors = np.array(vectors).astype('float32')
        dis, idx = instance.search(np_vectors, rk)
        return SUCCESS, dis, idx
    else:
        return VECTOR_EMPTY, None, None


def add(instance, ids, vectors):
    np_vectors = np.array(vectors).astype('float32')
    a, b, c, d = instance.add(np_vectors, ids)
    return SUCCESS, (a, b, c, d)


def reindex(instance, ids, vectors):
    vectors_np = np.array(vectors).astype('float32')
    a, b, c, d = instance.reindex(vectors_np, ids)
    return SUCCESS, (a, b, c, d)


def delete(instance, ids):
    a, b, c, d = instance.remove_by_ids(ids)
    return SUCCESS, (a, b, c, d)


def replace(instance, ids, vectors):
    pass


def meta(model_man, rc_id, is_obj=True):
    if model_man.contain(str(rc_id)):
        if is_obj:
            return SUCCESS, model_man.get(str(rc_id))
        else:
            return SUCCESS, model_man.get(str(rc_id)).to_string()
    else:
        return INDEX_NO_EXIST, None


def persit(context, man, rc_id):
    index_persit = context.contain['index_persit']
    index_persit.persit_one(man, rc_id)
