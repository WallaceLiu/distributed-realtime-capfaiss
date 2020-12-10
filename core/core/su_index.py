# -*- coding: utf-8 -*-
import faiss

from core.core.base_index import IndexBase
from core.utils.io_utils import is_exist, mkdir

PROCESS_COUNT = 4
faiss.omp_set_num_threads(PROCESS_COUNT)


class SimpleFlatIndex(IndexBase):
    def __init__(self, rc_id, params):
        IndexBase.__init__(self, rc_id, params)

    def train(self, matrix, ids_seq, ids):
        _index = faiss.index_factory(self.d, "IVF100,Flat", faiss.METRIC_INNER_PRODUCT)
        _index.nprobe = 20
        _index.train(matrix)
        _index.make_direct_map()
        self.ids_seq = ids_seq
        _index_with_id = faiss.IndexIDMap(_index)
        _index_with_id.add_with_ids(matrix, ids_seq)

        self.index = _index
        self.index_with_id = _index_with_id

    def save(self):
        if not is_exist(self.rc_path):
            mkdir(self.rc_path)
        faiss.write_index(self.index, self.file_path)
        faiss.write_index(self.index_with_id, self.id_map_path)
        self._write_seq_2_id()
