import unittest

import redis
import time
from concurrent.futures import ProcessPoolExecutor

r = redis.Redis(host='localhost', port=6379)

k = 'cupid-sim_sim_dmcqm_lhmx_sku_rec_faiss_item_vec_scene102002_v1_s_d_d100_e100-watcher'
v = {'id': 'e71bc544-7fa5-11ea-8249-8c85909d35fg', 'status': 0}

r.hmset(k, v)
a = r.hgetall(k)
print(a)
# 101001100=r.hmget(k,).hgetall(k)

