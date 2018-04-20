#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     etcdClient
   Description :
   Author :       Eason
   date：          2018/4/20
-------------------------------------------------
   Change Activity:
                   2018/4/20:
-------------------------------------------------
"""
import etcd

client = etcd.Client(host='10.15.144.131',port=2379)
# print(client.members)
print(client.get("").get_subtree)
# print(dir(etcd.EtcdResult))
# result = client.get("")

# print(result.children)
# print(result.dir)
# print(result.key)
# print(result.action)
# print(result.get_subtree())
# for r in result.get_subtree():
#     print(r)
#     print(r.get_subtree())
#     for rr in r.get_subtree():
#         print(rr)
#         i
# print(client.get("/config"))
# print(dir(client))
# print(client.members)
# print(client.key_endpoint())
# print(client.read("").key_point())
# for li in client.read("/nodes").get_subtree():
#     print(li)
# print(dir(etcd.EtcdResult))

# print(client.get("/codis3/default/slots"))
# print(client.read("/docker"))
# print(client.get("/nodes"))
# from etcd.client import Client
# c = Client(host='10.15.144.131',port=2379)
# print(client.get("/"))
# client.write('/nodesn1', 123)
# result = client.read('/nodesn1')
# print(result.value) # bar

