# import numpy as np
#
# from core.core.custom_index import CustomIndex
#
# d = 100
# nb = 10000
# xb = np.random.random((nb, d)).astype('float32')
# ids = np.arange(nb) + 1
#
# params = {'name': '搜索热搜', 'path': './index', 'dim': 100, 'oss_bucket_name': 'sim-model', 'extra': None, 'knn': 100,
#           'topn': -1, 'is_all': False, 'add_random': True,
#           'r2m': {'pin': 'cupid-sim-{pin}-{model_name}', 'item': 'cupid-sim-{item}-{model_name}',
#                   'req': 'cupid-sim-req-{pin}-{model_name}'}}
# f = CustomIndex(rc_id='101001101', params=params)
# f.reindex(xb, ids)
# print('f.shape', f.shape)
# #
# # nq = 1
# # xq = np.random.random((nq, d)).astype('float32')
# # xq = xb[:1]
# # D, I = f.search(xq, 10)
# #
# # print(D)
# # print(I)
# #
# # ids2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype='int64')
# # f.remove_ids(ids2)
# #
# # print('f.shape', f.shape)
