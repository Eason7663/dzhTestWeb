#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     singletonClass
   Description :
   Author :       Eason
   date：          2018/4/26
-------------------------------------------------
   Change Activity:
                   2018/4/26:
-------------------------------------------------
"""
import time
import threading
import paramiko


class JmeterServer():
    _instance_lock = threading.Lock()

    def __init__(self,host,username,password,path,port=22):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.path = path
        time.sleep(1)

    @classmethod
    def instance(cls, *args, **kwargs):
        with JmeterServer._instance_lock:
            if not hasattr(JmeterServer, "_instance"):
                JmeterServer._instance = JmeterServer(*args, **kwargs)
        return JmeterServer._instance

class LocalServer():
    _instance_lock = threading.Lock()

    def __init__(self,localPath,jmxName,step,loop=10):
        self.localPath = localPath
        self.jmxName = jmxName
        self.step = step
        self.loop = loop

    @classmethod
    def instance(cls, *args, **kwargs):
        with LocalServer._instance_lock:
            if not hasattr(JmeterServer, "_instance"):
                JmeterServer._instance = LocalServer(*args, **kwargs)
        return JmeterServer._instance


if __name__ =="__main__":
    host = "10.15.107.189"
    username = "root"
    password = "znzyjwqqlsjrghwy189"
    path = "/opt/apache-jmeter-3.2/bin/"

    def task(arg):
        obj = JmeterServer.instance(host,username,password,path)
        time.sleep(3)
        print(obj)
        # time.sleep(3)


    for i in range(10):
        t = threading.Thread(target=task, args=[i, ])
        t.start()
    time.sleep(1)
    obj = JmeterServer.instance()
    print(obj)

    # client = paramiko.SSHClient()