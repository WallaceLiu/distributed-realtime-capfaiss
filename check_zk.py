# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys

sys.path.append('core.zip')

import logging
import time
from config import context
from core.coordinate.HaMaster import HAMaster
from core.utils.utils import load_yaml

logger = logging.getLogger(__name__)
logging_config = load_yaml('./logging.yml')
logging.config.dictConfig(logging_config)
logger = logging.getLogger()

if __name__ == '__main__':
    ha = HAMaster(context.get_zkConfig(), context.contain['ducc'])
    ha.create_instance()
    ha.choose_master()
    while 1:
        time.sleep(10)
