#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     websocketSvrView
   Description :
   Author :       Eason
   date：          2018/5/4
-------------------------------------------------
   Change Activity:
                   2018/5/4:
-------------------------------------------------
"""
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse
import time

@accept_websocket
def echo(request):
    if not request.is_websocket():#判断是不是websocket连接
        pass
    #     request.websocket.send("hello")
    #     # try:#如果是普通的http方法
    #     #     message = request.GET['message']
    #     #     return HttpResponse(message)
    #     # except:
    #     #     return render(request,'pfmApp/websocketClient.html')
    else:
        # for message in request.websocket:
        for i in range(1,31):
            time.sleep(1)
            msg = str(i) + ": " + str(time.time())
            print(msg)
            request.websocket.send(str(msg)) #发送消息到客户端
            # for message in request.websocket:
            #     if message =='close':
            #         break

