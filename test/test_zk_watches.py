import sys
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.client import KeeperState

zk = KazooClient(hosts='127.0.0.1:2181', read_only=True)
zk.start()


@zk.add_listener
def watch_for_ro(state):
    if state == KazooState.CONNECTED:
        if zk.client_state == KeeperState.CONNECTED_RO:
            print("Read only mode!")
        else:
            print("Read/Write mode!")
    else:
        print('aaa')
