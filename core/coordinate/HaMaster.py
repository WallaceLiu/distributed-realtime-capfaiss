# -*- coding:utf-8 -*-
import logging
import socket
import pandas as pd
import numpy as np
import json
import traceback
from kazoo.client import KazooClient
from kazoo.client import KazooState
import time
from core.coordinate.MyScheduler import MyScheduler
from core.utils.utils import TODAY
from core.utils.udecorator import synchronized
from core.utils.ducc_utils import DuccClient


# from config import context


class HAMaster(object):
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, config, ducc):
        self.path = config['elect']
        self._ducc = ducc
        self.scheduler = MyScheduler()
        self.zk_config = config['hosts']
        logging.info('zk conn...%s' % self.zk_config)
        self.zk = KazooClient(self.zk_config, timeout=5)
        self.zk.start()
        self.zk.add_listener(self.my_listener)
        self.is_leader = False
        self.ip = socket.gethostbyname(socket.gethostname())

    def create_instance(self):
        node = self.path + '/' + self.ip + '-'
        self.zk.create(path=node, value=b"", ephemeral=True, sequence=True, makepath=True)

    def choose_master(self):
        logging.info("########## begin elect master ############")
        ip_seq_list = self.zk.get_children(path=self.path, watch=self.my_watcher)
        ip_addr = max(ip_seq_list).split('-')[0]

        if ip_addr == self.ip:
            req = self._ducc.update('elect', {
                "value": self.ip,
                "description": 'elect_master',
            })
            if not self.is_leader:
                self.scheduler.init_scheduler()
                self.is_leader = True
                logging.info("######### %s elected master, before it is not, register scheduler ##########" % ip_addr)
            else:
                logging.info(
                    "######### %s elected master, before it is, do not register scheduler ##########" % ip_addr)
        else:
            if self.is_leader:
                self.scheduler.stop_scheduler()
                self.is_leader = False
                logging.info("######### elected slave, before it is not, stop scheduler ##########")
            else:
                logging.info("######### elected slave, before is is, continue scheduler ##########")

        logging.info("########## elect master end ############")

    def my_listener(self, state):
        if state == KazooState.LOST:
            logging.info("########## session timeout: KazooState.LOST ############")

            while True:
                try:
                    self.create_instance()
                    self.zk.get_children(path=self.path, watch=self.my_watcher)
                    logging.info("########## session timeout: reconstruct session! ############")
                    break
                except Exception as ex:
                    # ex.print_exc()
                    pass
        elif state == KazooState.SUSPENDED:
            logging.info("########## session timeout: KazooState.SUSPENDED ############")

        elif state == KazooState.CONNECTED:
            logging.info("########## session timeout: KazooState.CONNECTED ############")

        else:
            logging.info("########## session timeout: Illegal KazooState ############")

    def my_watcher(self, event):
        if event.state == "CONNECTED" and event.type == "CREATED" or event.type == "DELETED" or event.type == "CHANGED" or event.type == "CHILD":
            logging.info("########## watcher child changed event ############")
            self.choose_master()
        else:
            logging.info("########## watcher unidentified event ############")

    # def get_ip_list(self):
    #     ip_seq_list = self.zk.get_children(path=self.path)
    #     return [str(ip_seq).split('-')[0] for ip_seq in ip_seq_list if str(ip_seq).split('-')[0] != self.ip]
    def get_ip_list(self):
        ip_seq_list = self.zk.get_children(path=self.path)
        ip_seq_arr = [[str(d).strip().split('-')[0], int(str(d).strip().split('-')[1])] for d in
                      ip_seq_list]
        ip_seq_np = np.array(ip_seq_arr)
        ip_seq_df = pd.DataFrame(ip_seq_np, columns=['ip', 'seq'], index=range(len(ip_seq_arr)))
        ip_seq_df = ip_seq_df.groupby(ip_seq_df['ip']).max().reset_index()
        ip_list = list(ip_seq_df['ip'].values)
        return [ip for ip in ip_list if ip != self.ip]

    def get_master(self):
        ip_seq_list = self.zk.get_children(path=self.path)
        ip_addr = max(ip_seq_list).split('-')[0]
        return ip_addr
