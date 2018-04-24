#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     myThread
   Description :
   Author :       Eason
   date：          2018/4/24
-------------------------------------------------
   Change Activity:
                   2018/4/24:
-------------------------------------------------
"""
from appaction.jmeterServer import JmeterServer
import threading
from queue import Queue
import time,random

class JmeterThread(threading.Thread):
    taskQueue = Queue()
    def __init__(self,i):
        threading.Thread.__init__(self)
        # self.jmeterSvr = jmeterSvr
        self.i = i

    def run(self):
        # self.jmeterSvr.run_cmd()
        ii = random.randint(0,self.i)
        time.sleep(ii)

        s = "sleep " + ii + "s"
        self.taskQueue.put(s)


if __name__=="__main__":

    for i in range(10):


    JmeterThread.taskQueue.put(1)
    JmeterThread.taskQueue.put(2)
    JmeterThread.taskQueue.put(4)
    JmeterThread.taskQueue.put(2)
    print('LILO队列', JmeterThread.taskQueue)  # 查看队列中的所有元素
    print(JmeterThread.taskQueue.get())  # 返回并删除队列头部元素
    print(JmeterThread.taskQueue.queue)