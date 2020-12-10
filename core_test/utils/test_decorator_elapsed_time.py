# -*- coding: utf-8 -*-
from core.utils.udecorator import *


@elapsed_time
def test1():
    time.sleep(1)
    return 'aaa'


A = test1()
print(A)

import time

