# -*- coding: utf-8 -*-
from core.utils.udecorator import *
import time


@asynchronous
def long_process(num):
    time.sleep(10)
    return num * num


result = long_process.start(12)

for i in range(20):
    print(i)
    time.sleep(1)

    if result.is_done():
        print("result {0}".format(result.get_result()))

result2 = long_process.start(13)

try:
    print("result2 {0}".format(result2.get_result()))

except asynchronous.NotYetDoneException as ex:
    print(ex.message)
