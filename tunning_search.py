# -*- coding: utf-8 -*-
import sys

sys.path.append('core.zip')

import numpy as np
from config import model_man
from core.rc import *
from core.utils.udecorator import *
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

_, instance = meta(model_man, 101001101)
start_time = datetime.datetime.now()
v1, v2, v3 = search(instance, xb[:1], 2000)
over_time = datetime.datetime.now()
etime = (over_time - start_time).total_seconds()
# print(v1)
# print(v2)
# print(v3)
print('Elapsed time: current function is {0} s'.format(etime))
