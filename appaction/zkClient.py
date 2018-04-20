#!/usr/bin/python
"""
-------------------------------------------------
   File Name：     zkClient
   Description :
   Author :       Eason
   date：          2018/4/20
-------------------------------------------------
   Change Activity:
                   2018/4/20:
-------------------------------------------------
"""

from kazoo.client import KazooClient


class PyZooConn(object):
    # init function include connection method
    def __init__(self):
        self.zk = KazooClient(hosts='10.15.107.110:2181')
        self.zk.start()

        # get node data

    def get_data(self, param):
        result = self.zk.get(param)
        print(result)

        # create a node and input a value in this node

    def create_node(self, node, value):
        self.zk.create(node, value)

        # close the connection

    def close(self):
        self.zk.stop()

    ''''' 
    Hypothesis there is a bunch of methods here haha :) 
    '''


if __name__ == '__main__':
    # pz = PyZooConn()
    # value = b'theValue'
    # pz.create_node("/test123", value)
    # pz.get_data("/controller/")
    # pz.close()

    zk = KazooClient(hosts='10.15.144.74:2181')
    zk.start()
    children = zk.get("/docker_root_statusv2/cm5/hub_sys_bus_log_1")

    print(children)
    # for li in children:
    #     print(li)
    #     print(zk.get(li))
    # zk.get("/action/cm5/")
    zk.stop()