# -*- coding:utf-8 -*-
import time

from core.coordinate.HaMaster import HAMaster

ha = HAMaster()
# 向zk注册自己
ha.create_instance()
# 进行选主
ha.choose_master()

while 1:
    time.sleep(10)
