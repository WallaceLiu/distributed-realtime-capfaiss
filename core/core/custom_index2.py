# -*- coding: utf-8 -*-
import faiss

from core.core.base_index import IndexBase
from core.utils.io_utils import is_exist, mkdir



class FaissTrainIndex(IndexBase):
    def __init__(self):
        pass

    def train(self, xb):
        assert not self.index_with_id.is_trained
        self.index_with_id.train(xb)
        assert self.index_with_id.is_trained

    def ntotal(self):
        return self.index_with_id.ntotal

    def dim(self):
        return self.index_with_id.d

    def save(self, filepath):
        faiss.write_index(self.index_with_id, filepath)

    def reset(self):
        self.index_with_id.reset()
        self.index_with_id = None

    def set_nprobe(self, nprobe):
        faiss.ParameterSpace().set_index_parameter(self.index_with_id, "nprobe", nprobe)


class FaissFastIndex(FaissTrainIndex):
    def __init__(self, d):
        nlist = 100
        quantizer = faiss.IndexFlatL2(d)
        self.index_with_id = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)

        # https://github.com/facebookresearch/faiss/wiki/Faiss-code-structure#object-ownership
        self.index_with_id.own_fields = True
        quantizer.this.disown()

        self.index_with_id.nprobe = 10


class FaissShrinkedIndex(FaissTrainIndex):
    # nlist  numCentroids
    # m     number of subquantizers
    def __init__(self, d, nlist=4096, m=32):
        quantizer = faiss.IndexFlatL2(d)
        self.index_with_id = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)

        # self.index_with_id.own_fields = True
        # quantizer.this.disown()
        self.quantizer = quantizer

        self.index_with_id.nprobe = 32

    def reset(self):
        self.quantizer.reset()
        self.quantizer = None
        self.index_with_id.reset()
        self.index_with_id = None


class FaissShrinkedindexWithId(FaissTrainIndex):
    def __init__(self, d, nlist=100):
        self.index = faiss.IndexPQ(d, 16, 8)
        self.index.nprobe = 10
        self.index_with_id = faiss.IndexIDMap(self.index)


class FaissOPQIndex(FaissTrainIndex):
    def __init__(self, d, nlist=100):
        self.index_with_id = faiss.index_factory(d, 'OPQ32_128,IVF4096,PQ32')
        self.index_with_id.nprobe = 16


class FaissPCAIndex(FaissTrainIndex):
    def __init__(self, d):
        d2 = 256
        nlist = 100  # numCentroids
        m = 8  # numQuantizers

        coarse_quantizer = faiss.IndexFlatL2(d2)
        sub_index = faiss.IndexIVFPQ(coarse_quantizer, d2, nlist, 16, 8)
        pca_matrix = faiss.PCAMatrix(d, d2, 0, True)
        self.index_with_id = faiss.IndexPreTransform(pca_matrix, sub_index)

        sub_index.own_fields = True
        coarse_quantizer.this.disown()

        self.sub_index = sub_index
        self.pca_matrix = pca_matrix

        self.index_with_id.nprobe = 10


if __name__ == '__main__':
    import numpy as np

    d = 2048
    nb = 10
    xb = np.random.random((nb, d)).astype('float32')
    ids = np.arange(nb) + 1

    # print(xb)
    # print(ids)

    index = faiss.IndexFlatIP(d)
    # index_with_id = faiss.IndexIDMap2(index)
    index_with_id = faiss.IndexIDMap(index)
    # index_with_id.
    # faiss_index = FaissIndex(d)
    # faiss_index.add(xb, ids)
    # print(faiss_index.ntotal())
    #
    nq = 1
    xq = np.random.random((nq, d)).astype('float32')
    xq = xb[:1]
    # print(xq)
    # D, I = faiss_index.search(xq)
    # print(zip(I[0], D[0]))
