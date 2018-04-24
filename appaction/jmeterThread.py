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
# from appaction.jmeterServer import JmeterServer
import threading
from queue import Queue
import time,random,math

taskQueue = Queue()
# class JmeterThread(threading.Thread):
#
#     def __init__(self,i):
#         threading.Thread.__init__(self)
#         # self.jmeterSvr = jmeterSvr
#         self.i = i
#
#     def run(self):
#         # self.jmeterSvr.run_cmd()
#         ii = random.randint(0,self.i)
#         time.sleep(ii)
#
#         s = "sleep " + ii + "s"
#         self.taskQueue.put(s)

class odd():
    def __init__(self,num):
        self.num = num

    def __str__(self):
        return "I({}) am a odd".format(str(self.num))


class even():
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return "I({}) am a even".format(str(self.num))

def worker(name):

    ii = random.randint(0, 20)
    # time.sleep(ii)

        # s = name + " sleep " + str(ii) + "s"
    print("In thread: " + threading.current_thread().getName())
    if (ii%2)==0:
        print(ii)
        # even(ii)
        taskQueue.put(even(ii))
    else:
        # odd(ii)
        taskQueue.put(odd(ii))


if __name__=="__main__":
    for i in range(10):
        t = threading.Thread(target=worker,args=("Thread{}".format(i),),name="Thread"+str(i))
        t.start()
    j = 5
    while True:
        time.sleep(3)
        if j <=0 :
            break
        j -= 1
        tt = taskQueue.get()
        if isinstance(tt,odd):
            print("***odd:"+ tt.__str__())
        else:
            print("***even:"+ tt.__str__())
