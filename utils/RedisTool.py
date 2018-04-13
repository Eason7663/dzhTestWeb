#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     RedisTool
   Description :
   Author :       Eason
   date：          2018/3/21
-------------------------------------------------
   Change Activity:
                   2018/3/21:
-------------------------------------------------
"""
import redis
import time

def delKeys(hostip, keyPrefix):
    '''删除指定前缀的key'''
    for ip in hostip:
        print(ip)
        for key, value in ip.items():
            print("key : " + str(key))
            print("value : " + str(value))

            r = redis.Redis(host=key, port=value, db=0)
            for pre in keyPrefix:

                list = r.keys(pre)
                if len(list) == 0:
                    print("Not found:" + str(pre))
                    # time.sleep(3)
                else:
                    for i in list:
                        print(i)
                        r.delete(i)

                    print(len(list))


def findMaster(clusterIp):
    '''找出集群中的master'''
    hostIp = []
    port = [7000,7001]
    for ip in clusterIp:
        for p in port:
            r = redis.Redis(host=ip, port=p, db=0)
            data = r.execute_command('role')
            # print data
            if data[0] == 'master':
                tmp = {}
                tmp[ip] = p
                hostIp.append(tmp)

    return hostIp


if __name__ == "__main__":
    #内网视吧环境redis cluster地址，发生主从切换后，需要找到所有主节点，方可完成写或者删除key的操作
    clusterIp = {'10.15.107.83', '10.15.107.151', '10.15.107.150', '10.15.107.149', '10.15.107.179', '10.15.107.180'}
    #指定key的前缀列表
    keyPrefix = ['c80*','c90*','d0*','d10*','d20*','d30*','d40*','d50*','d60*','d70*','d80*']

    hostip = findMaster(clusterIp)
    delKeys(hostip, keyPrefix)