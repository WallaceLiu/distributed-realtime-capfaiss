# -*- coding: utf-8 -*-
import numpy as np
from config import model_man
from core.rc import *
import math

d = 100
nb = 2000
np.random.seed(4567)
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 2000.

ids = ['u' + str(i + nb) for i in range(1, nb + 1)]

N, dim = xb.shape
x = int(4 * math.sqrt(N))
train_count = min(64 * x, N)
print(x, train_count)
_, instance = meta(model_man, 101001101)
status, result = reindex(instance, ids, xb)
print(status)
print(result)
