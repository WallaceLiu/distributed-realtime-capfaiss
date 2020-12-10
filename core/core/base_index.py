# -*- coding: utf-8 -*-
import json
import logging

import faiss
import numpy as np

from core.utils.io_utils import is_exist, write, read
from core.utils.udecorator import elapsed_time

PROCESS_COUNT = 4
faiss.omp_set_num_threads(PROCESS_COUNT)


class IndexBase:
    def __init__(self, rc_id, params):
        self.rc_id = rc_id
        self.params = params
        self.path = params['path']
        self.rc_path = "%s/%s" % (self.path, self.rc_id)
        self.file_path = "%s/%s.idx" % (self.rc_path, self.rc_id)
        self.id_map_path = "%s/%s.map.idx" % (self.rc_path, self.rc_id)
        self.ids_seq = None
        self.ids_path = "%s/%s.mapper" % (self.rc_path, self.rc_id)
        self.d = params['dim']
        self.seq_2_id = {}
        self.id_2_seq = {}
        self.action = None
        self.status = False
        self.index = None
        self.index_with_id = None

    @property
    def ntotal(self):
        if self.index is not None:
            return self.index_with_id.ntotal
        else:
            return None

    @property
    def dim(self):
        return self.index.d

    @property
    def shape(self):
        return self.ntotal, self.dim

    def train(self, matrix, ids_seq, ids):
        pass

    @elapsed_time
    def search(self, xq, k):
        # @elapsed_time
        def _real_ids():
            return [self.seq_2_id[str(i)] for i in list(idx)[0] if str(i) in self.seq_2_id.keys()]

        self.index_with_id.nprobe = 20
        dis, idx = self.index_with_id.search(xq, k)
        logging.info('orgin search count: {0}'.format(self.ntotal))
        ids = _real_ids()  # [self.seq_2_id[str(i)] for i in list(idx)[0] if str(i) in self.seq_2_id.keys()]
        return list(dis[0]), ids

    def add(self, xb, ids):
        ids_seq = np.arange(self.ntotal, self.ntotal + xb.shape[0]) + 1
        before_ntotal = self.ntotal
        for seq, i in zip(list(ids_seq), ids):
            self.seq_2_id[str(seq)] = i
            self.id_2_seq[str(i)] = seq
        self.index_with_id.add_with_ids(xb, ids_seq)
        after_ntotal = self.ntotal
        return (before_ntotal, after_ntotal, len(ids_seq), len(ids_seq))

    def reindex(self, xb, ids):
        self.reset()
        ids_seq = np.arange(xb.shape[0]) + 1
        self.train(xb, ids_seq, ids)
        self._create_mapper(ids_seq, ids)
        self.save()
        return (0, self.ntotal, self.ntotal, self.ntotal)

    def remove_by_ids(self, ids):
        ids_seq = [self.id_2_seq[k] for k in ids if k in self.id_2_seq.keys()]  # id 2 seq
        # print('enter remove_by_ids...ids_seq=%s,', len(ids_seq), ids_seq)
        before_ntotal = self.ntotal
        after_ntotal = self.ntotal
        expected = len(ids)
        actual = 0
        if len(ids_seq) > 0:
            # try:
            before_ntotal, after_ntotal, actual = self.remove_by_ids_seq(ids_seq)
            expected = len(ids)

            for k in ids:
                if k in self.id_2_seq.keys():
                    del self.id_2_seq[k]
            for v in ids_seq:
                if v in self.seq_2_id.values():
                    del self.seq_2_id[k]
            # except Exception as ex:
            #     pass

        # print('enter remove_by_ids before_ntotal=%s, after_ntotal=%s, expected=%s, actual=%s', before_ntotal,
        #       after_ntotal, expected, actual)
        return (before_ntotal, after_ntotal, expected, actual)

    def remove_by_ids_seq(self, ids_seq):
        # print('enter remove_by_ids_seq...v=%s', len(ids_seq))
        before_ntotal = self.ntotal
        ids_seq_np = np.array(ids_seq).astype('int64')
        self.index_with_id.remove_ids(ids_seq_np)
        after_ntotal = self.ntotal
        actual = len(ids_seq)
        # print('enter remove_by_ids_seq before_ntotal=%s, after_ntotal=%s, actual=%s', before_ntotal,
        #       after_ntotal, actual)
        return (before_ntotal, after_ntotal, actual)

    def restore(self):
        if self.file_path is not None and len(self.file_path) > 0 and is_exist(self.file_path) \
                and self.id_map_path is not None and len(self.id_map_path) > 0 and is_exist(self.id_map_path):
            logging.info('restore file_path...%s' % self.file_path)
            self.index = faiss.read_index(self.file_path)
            self.index_with_id = faiss.read_index(self.id_map_path)
            logging.info('restore id_mapper_path...%s' % self.ids_path)
            self._read_seq_2_id()
            self.status = True
            return True
        else:
            return False

    def reset(self):
        # self.index.reset()
        self.index = None
        # self.index_with_id.reset()
        self.index_with_id = None

    def save(self):
        pass

    def _create_mapper(self, ids_seq, ids):
        if len(ids_seq) > 0 and len(ids) > 0:
            for seq, i in zip(list(ids_seq), list(ids)):
                self.seq_2_id[str(seq)] = str(i)
                self.id_2_seq[str(i)] = str(seq)

    def _write_seq_2_id(self):
        write(self.ids_path, json.dumps(self.seq_2_id))

    def _read_seq_2_id(self):
        logging.info('read seq 2 ids...')
        if is_exist(self.ids_path):
            c = read(self.ids_path)
            if c is not None:
                self.seq_2_id = eval(c[0])
                for k in self.seq_2_id.keys():
                    self.id_2_seq[str(self.seq_2_id[k])] = k

    def to_string(self):
        return "%s, %s" % (self.rc_id, self.file_path)
