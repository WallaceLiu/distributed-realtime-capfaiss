# -*- coding: utf-8 -*-

from concurrent import futures
import logging

import grpc
import time
import json
from config import context as _context, model_man
from core.grpc import syncindex_pb2
from core.grpc import syncindex_pb2_grpc
from core.rc import add, delete, reindex, meta, search
from core.uconstant.response_code import *
from core.grpc.syncindex_utils import internalArray_2_vector


def _get_ha():
    return _context.contain['ha']


class SyncIndex(syncindex_pb2_grpc.SyncIndexServicer):

    def Greeting(self, request, context):
        return syncindex_pb2.SyncReply(code=200, message='greeting', data=None)

    def Search(self, request, context):
        status, instance = meta(model_man, request.rcId)
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=None)

        status, result = search(instance, request.vectors, request.k)

        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))

        return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))

    def Meta(self, request, context):
        return syncindex_pb2.SyncReply(code=200, message='not support', data=None)

    def Reindex(self, request, context):
        status, instance = meta(model_man, request.rcId)
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=None)

        status, result = reindex(instance, request.ids, internalArray_2_vector(request.vectors))
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=None)

        return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))

    def Add(self, request, context):
        status, instance = meta(model_man, request.rcId)
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=None)

        status, result = add(instance, request.ids, internalArray_2_vector(request.vectors))
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))

        return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))

    def Delete(self, request, context):
        status, instance = meta(model_man, request.rcId)
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=None)

        status, result = delete(instance, request.ids)
        if status != SUCCESS:
            return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))

        return syncindex_pb2.SyncReply(code=status, message=RESPONSE_CODE[status], data=str(result))


def SyncIndexServe():
    options = [('grpc.max_send_message_length', 100 * 1024 * 1024),
               ('grpc.max_receive_message_length', 100 * 1024 * 1024),
               ('grpc.max_message_length', 100 * 1024 * 1024)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    syncindex_pb2_grpc.add_SyncIndexServicer_to_server(SyncIndex(), server)
    host = _context.get_rpcConfig()['slave']['host']
    port = _context.get_rpcConfig()['slave']['port']
    server.add_insecure_port('{host}:{port}'.format(host=host, port=port))
    server.start()
    while 1:
        time.sleep(10)
