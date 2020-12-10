import unittest

import redis
import time
from concurrent.futures import ProcessPoolExecutor

r = redis.Redis(host='localhost', port=6379)

# with r.pipeline(transaction=False) as p:
#     p.set('1', '101001100').set('2', 'b').set('3', 'c')
#     p.execute()

result = None

a = ['1', '2', '3','101001100']

with r.pipeline(transaction=False) as p:
    for d in a:
        p.get(d)
    result = p.execute()
print(result)
