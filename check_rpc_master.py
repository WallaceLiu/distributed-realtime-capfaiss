# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import sys

sys.path.append('core.zip')

import grpc
from core.grpc import syncindex_pb2
from core.grpc import syncindex_pb2_grpc
import numpy as np
import argparse
from config import context
from core.grpc_ser.syncindex_server_master import vector_2_internalArray

logging.basicConfig()


def test_greeting_rpc(host, port):
    with grpc.insecure_channel('%s:%s' % (host, port)) as channel:
        stub = syncindex_pb2_grpc.SyncIndexStub(channel)
        response = stub.Greeting(syncindex_pb2.SyncRequest(rcId='1', ids=[], vectors=None))
    return response


def test_reindex_rpc(host, port, rc_id, xb, ids):
    with grpc.insecure_channel('%s:%s' % (host, port)) as channel:
        stub = syncindex_pb2_grpc.SyncIndexStub(channel)
        response = stub.Reindex(syncindex_pb2.SyncRequest(rcId=str(rc_id),
                                                          ids=ids,
                                                          k=0,
                                                          vectors=vector_2_internalArray(list(xb))))
    return response


def test_add_rpc(host, port, rc_id, xb, ids):
    with grpc.insecure_channel('%s:%s' % (host, port)) as channel:
        stub = syncindex_pb2_grpc.SyncIndexStub(channel)
        response = stub.Add(syncindex_pb2.SyncRequest(rcId=str(rc_id),
                                                      ids=ids,
                                                      vectors=vector_2_internalArray(list(xb))))
    return response


def test_del_rpc(host, port, rc_id, ids):
    with grpc.insecure_channel('%s:%s' % (host, port)) as channel:
        stub = syncindex_pb2_grpc.SyncIndexStub(channel)
        response = stub.Delete(syncindex_pb2.SyncRequest(rcId=str(rc_id), ids=ids))
    return response


def replace():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', required=False, help='Initial learning rate')
    parser.add_argument('--rc_id', type=int, default=101001101, required=False, help='Initial learning rate')
    params = parser.parse_args()

    d = 100
    nb = 2000
    np.random.seed(1234)
    xb = np.random.random((nb, d)).astype('float32')
    xb[:, 0] += np.arange(nb) / 1000.

    ids = ['u' + str(i) for i in range(nb)]

    port = context.get_rpcConfig()['master']['port']

    req = test_greeting_rpc(params.host, port)

    # reindex
    print('reindex...')
    req = test_reindex_rpc(params.host, port, params.rc_id, xb, ids)

    print(req)

    # delete
    print('delete...')
    req = test_del_rpc(params.host, port, params.rc_id, ids[:10])

    print(req)

    # add
    d = 100
    nb = 2000
    np.random.seed(5678)
    xb = np.random.random((nb, d)).astype('float32')
    xb[:, 0] += np.arange(nb) / 1000.

    ids = ['u' + str(i) for i in range(nb, nb + 2000)]

    print('add...')
    req = test_add_rpc(params.host, port, params.rc_id, xb, ids)

    print(req)
