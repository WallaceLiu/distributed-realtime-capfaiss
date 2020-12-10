import numpy as np

import faiss
import json


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


index = faiss.IndexFlat(100)
xb = np.zeros((2000, 100), dtype='float32')
xb[:, 0] = np.arange(2000, dtype='int64') + 1000
# print('xb', xb)
index.add(xb)
# print(index.ntotal, index.d)

# del_ids = np.arange(5, dtype='int64') * 2
# print('del_ids', del_ids)
#
# index.remove_ids(del_ids)

# xb2 = faiss.vector_float_to_array(index.xb)  # .reshape(10, 5)
# faiss.
#
# print('index.xb.shape', index.reconstruct())
# print('xb2', xb2.shape)
v = index.reconstruct_n(0, index.ntotal)
# print(type(v))
v_str = json.dumps(v, cls=NpEncoder)
# print(v_str)

d = {}
d['rcId'] = '101001101'
d['vectors'] = json.loads(v_str)
print(json.dumps(d))
# print(index.xb)
# index.
