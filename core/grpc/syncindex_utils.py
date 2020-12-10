from core.grpc import syncindex_pb2


def vector_2_internalArray(vectors):
    rpc_vectors = []
    for vector in vectors:
        rpc_vectors.append(syncindex_pb2.InternalArray(vector=vector))
    return rpc_vectors


def internalArray_2_vector(internalVectors):
    vectors = []
    for v in internalVectors:
        vectors.append(v.vector)
    return vectors
