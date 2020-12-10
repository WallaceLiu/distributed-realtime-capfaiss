# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys

sys.path.append('core.zip')

import logging
from config import context
from core.grpc_ser.syncindex_server_master import SyncMasterIndexServe
from core.utils.utils import load_yaml

logger = logging.getLogger(__name__)
logging_config = load_yaml('./logging-rpc.yml')
logging.config.dictConfig(logging_config)
logger = logging.getLogger()

if __name__ == '__main__':
    SyncMasterIndexServe()
