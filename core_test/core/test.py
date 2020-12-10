import numpy as np

import faiss

# def create_faiss_model(matrix, item_list, faiss_path, params="IVF100,Flat", size=100, mode="train"):
#     matrix = np.array(matrix, dtype=np.float32)
#     ids = np.array(item_list).astype("int")
#     # if mode == "train":
#     index = faiss.index_factory(size, params, faiss.METRIC_INNER_PRODUCT)
#     index.nprobe = 20
#     index.train(matrix)
#     index.make_direct_map()
#     index_id = faiss.IndexIDMap(index)
#     # elif mode == "update":
#     #     index_id = faiss.read_index(faiss_path)
#     index_id.add_with_ids(matrix, ids)
#
#     # index保存
#     faiss.write_index(index_id, faiss_path)
#
#     return index

d = 100
nb = 1000
xb = np.random.random((nb, d)).astype('float32')
ids = np.arange(nb) + 1

index = faiss.index_factory(d, "Flat", faiss.METRIC_INNER_PRODUCT)
index.nprobe = 20
index.train(xb)
# index.make_direct_map()

indexWithId = faiss.IndexIDMap(index)
indexWithId.add_with_ids(xb, ids)

nq = 1
xq = np.random.random((nq, d)).astype('float32')
xq = xb[:1]
D, I = index.search(xq, 10)
print('D', D)
print('I', I)

#
# ids2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype='int64')
# indexWithId.remove_ids(ids2)
#

# print(index.d, index.ntotal)




# indexWithId.remove_ids(np.array([103], dtype='int64'))
#
# nq = 1
# xq = np.random.random((nq, d)).astype('float32')
# xq = xb[:1]
# # D, I = f.search(xq, 10)
#
# # print(D)
# # print(I)
#
# # 101001100 = np.arange(5)
# # print(101001100.shape)
#
#
# # index.remove_ids(np.array([103], dtype='int64'))
#
# ids2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype='int64')
# # print(ids2.shape)
# # f.remove_ids(ids2)
