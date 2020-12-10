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
import json
from config import model_man, context  # , cache_r2m, cache_r2mp
from core.uconstant.response_code import *
from core.uconstant.response_code import SUCCESS
from core.grpc import syncindex_pb2
from core.grpc import syncindex_pb2_grpc
from core.rc import meta as _meta
import grpc
from core.grpc_ser.syncindex_server_master import vector_2_internalArray


def get_elect_master():
    ducc = context.contain['ducc']
    req = ducc.query('elect')
    obj = json.loads(req.content)
    data = obj['data']
    elect_master = data['value']
    return elect_master


def meta(ha, rc_id):
    if ha.is_leader:
        status, instance = _meta(model_man, rc_id)
        return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=instance)

    elect_master = get_elect_master()
    with grpc.insecure_channel('%s:50051' % elect_master) as channel:
        stub = syncindex_pb2_grpc.SyncIndexStub(channel)
        response = stub.Meta(syncindex_pb2.SyncRequest(rcId=rc_id))
    return {'code': SUCCESS, 'msg': RESPONSE_CODE[SUCCESS], 'data': str(response)}


def add(ha, rc_id, ids, vectors):
    def _add(host, port, rc_id, ids, vectors):
        vs = vector_2_internalArray(vectors)
        with grpc.insecure_channel('%s:%s' % (host, port)) as channel:
            stub = syncindex_pb2_grpc.SyncIndexStub(channel)
            response = stub.Add(syncindex_pb2.SyncRequest(rcId=rc_id, ids=ids, vectors=vs))
        return {'code': SUCCESS, 'msg': RESPONSE_CODE[SUCCESS], 'data': str(response)}

    port = context.get_rpcConfig()['master']['port']

    if ha.is_leader:
        result = _add('localhost', port, rc_id, ids, vectors)
        return result
    else:
        elect_master = get_elect_master()
        result = _add(elect_master, port, rc_id, ids, vectors)
        return result


def reindex(ha, rc_id, ids, vectors):
    def _reindex(host, port, rc_id, ids, vectors):
        vs = vector_2_internalArray(vectors)
        with grpc.insecure_channel('%s:%s' % (host, port)) as channel:
            stub = syncindex_pb2_grpc.SyncIndexStub(channel)
            response = stub.Reindex(syncindex_pb2.SyncRequest(rcId=rc_id, ids=ids, vectors=vs))
        return {'code': SUCCESS, 'msg': RESPONSE_CODE[SUCCESS], 'data': str(response)}

    port = context.get_rpcConfig()['master']['port']

    if ha.is_leader:
        result = _reindex('localhost', port, rc_id, ids, vectors)
        return result
    else:
        elect_master = get_elect_master()
        result = _reindex(elect_master, port, rc_id, ids, vectors)
        return result


def delete(ha, rc_id, ids):
    def _del(host, port, rc_id, ids):
        with grpc.insecure_channel('%s:%s' % (host, port)) as channel:
            stub = syncindex_pb2_grpc.SyncIndexStub(channel)
            response = stub.Delete(syncindex_pb2.SyncRequest(rcId=rc_id, ids=ids))
        return {'code': SUCCESS, 'msg': RESPONSE_CODE[SUCCESS], 'data': str(response)}

    # print('aaaaaa delete enter')
    port = context.get_rpcConfig()['master']['port']

    if ha.is_leader:
        # print('aaaaaa delete localhost')
        result = _del('localhost', port, rc_id, ids)
        return result
    else:
        elect_master = get_elect_master()
        # print('aaaaaa delete %s' % elect_master)
        result = _del(elect_master, port, rc_id, ids)
        return result


def replace(instance, ids, vectors):
    pass
