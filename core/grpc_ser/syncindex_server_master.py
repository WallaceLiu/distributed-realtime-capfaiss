# -*- coding: utf-8 -*-

from concurrent import futures
import logging

import grpc
import time
from config import context as _context, model_man
from core.grpc import syncindex_pb2
from core.grpc import syncindex_pb2_grpc
from core.rc import add, delete, reindex, meta, persit, search
from core.uconstant.response_code import *
from core.grpc.syncindex_utils import vector_2_internalArray, internalArray_2_vector


def _get_ha():
    return _context.contain['ha']


class SyncMasterIndex(syncindex_pb2_grpc.SyncIndexServicer):

    def Greeting(self, request, context):
        return syncindex_pb2.SyncReply(code=200, message='master greeting', data=None)

    def Search(self, request, context):
        return syncindex_pb2.SyncReply(code=200, message='not support', data=None)

    def Meta(self, request, context):
        status, instance = meta(_context.contain['model_man'], request.rcId)
        return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=instance)

    def Reindex(self, request, context):
        def _para():
            pass

        ha = _get_ha()
        status, instance = meta(model_man, request.rcId)

        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=None)

        vs = internalArray_2_vector(request.vectors)
        status, result = reindex(instance, request.ids, vs)
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=None)

        persit(_context, model_man, request.rcId)

        response = syncindex_pb2.SyncReply(code=SUCCESS, message=RESPONSE_CODE[SUCCESS], data=str(result))

        response_list = []
        response_list.append({'host': 'localhost', 'resp': str(response)})

        hosts = ha.get_ip_list()
        port = _context.get_rpcConfig()['slave']['port']

        if len(hosts) > 0:
            for rpc_host in hosts:
                options = [('grpc.max_send_message_length', 100 * 1024 * 1024),
                           ('grpc.max_receive_message_length', 100 * 1024 * 1024),
                           ('grpc.max_message_length', 100 * 1024 * 1024)]
                with grpc.insecure_channel('%s:%s' % (rpc_host, port), options=options) as channel:
                    stub = syncindex_pb2_grpc.SyncIndexStub(channel)
                    response = stub.Reindex(syncindex_pb2.SyncRequest(rcId=request.rcId,
                                                                      ids=request.ids,
                                                                      vectors=request.vectors))
                    response_list.append({'host': rpc_host, 'resp': str(response)})
        return syncindex_pb2.SyncReply(code=SUCCESS, message=RESPONSE_CODE[SUCCESS], data=str(response_list))

    def Add(self, request, context):
        ha = _get_ha()
        response_list = []
        status, instance = meta(model_man, request.rcId)
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=None)

        status, result = add(instance, request.ids, internalArray_2_vector(request.vectors))
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))

        persit(_context, model_man, request.rcId)

        response = syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))
        response_list.append({'host': 'localhost', 'resp': str(response)})

        hosts = ha.get_ip_list()
        port = _context.get_rpcConfig()['slave']['port']

        if len(hosts) > 0:
            for rpc_host in hosts:
                options = [('grpc.max_send_message_length', 100 * 1024 * 1024),
                           ('grpc.max_receive_message_length', 100 * 1024 * 1024),
                           ('grpc.max_message_length', 100 * 1024 * 1024)]
                with grpc.insecure_channel('%s:%s' % (rpc_host, port), options=options) as channel:
                    stub = syncindex_pb2_grpc.SyncIndexStub(channel)
                    response = stub.Add(
                        syncindex_pb2.SyncRequest(rcId=request.rcId, ids=request.ids, vectors=request.vectors))
                    response_list.append({'host': rpc_host, 'resp': str(response)})
        return syncindex_pb2.SyncReply(code=SUCCESS, message=RESPONSE_CODE[SUCCESS], data=str(response_list))

    def Delete(self, request, context):
        ha = _get_ha()
        response_list = []
        status, instance = meta(model_man, request.rcId)
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=None)

        status, result = delete(instance, request.ids)
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=result)

        persit(_context, model_man, request.rcId)

        response = syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))
        response_list.append({'host': 'localhost', 'resp': str(response)})

        hosts = ha.get_ip_list()
        port = _context.get_rpcConfig()['slave']['port']

        if len(hosts) > 0:
            for rpc_host in hosts:
                with grpc.insecure_channel('%s:%s' % (rpc_host, port)) as channel:
                    stub = syncindex_pb2_grpc.SyncIndexStub(channel)
                    response = stub.Delete(syncindex_pb2.SyncRequest(rcId=request.rcId, ids=request.ids))
                    response_list.append({'host': rpc_host, 'resp': str(response)})
        return syncindex_pb2.SyncReply(code=SUCCESS, message=RESPONSE_CODE[SUCCESS], data=str(response_list))


def SyncMasterIndexServe():
    options = [('grpc.max_send_message_length', 100 * 1024 * 1024),
               ('grpc.max_receive_message_length', 100 * 1024 * 1024),
               ('grpc.max_message_length', 100 * 1024 * 1024)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    syncindex_pb2_grpc.add_SyncIndexServicer_to_server(SyncMasterIndex(), server)
    host = _context.get_rpcConfig()['master']['host']
    port = _context.get_rpcConfig()['master']['port']
    server.add_insecure_port('{host}:{port}'.format(host=host, port=port))
    server.start()
    while 1:
        time.sleep(10)
