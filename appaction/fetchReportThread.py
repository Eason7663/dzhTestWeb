#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     fetchReportThread
   Description :
   Author :       Eason
   date：          2018/4/25
-------------------------------------------------
   Change Activity:
                   2018/4/25:
-------------------------------------------------
"""
import threading
import paramiko
from queue import Queue
msgQueue = Queue()

class JmeterServer():
    def __init__(self,host,username,password,path,port=22):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.path = path

class FetchReportThread(threading.Thread):
    def __init__(self,jmeterServer,reportName,threadName):
        threading.Thread.__init__(self)
        self.jmeterServer =jmeterServer
        self.reportName =reportName
        self.name = threadName
        self.host = jmeterServer.host
        self.port = jmeterServer.port
        self.username = jmeterServer.username
        self.password = jmeterServer.password
        self.path = jmeterServer.path
        self.obj = paramiko.SSHClient()
        self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.obj.connect(self.host,self.port,self.username,self.password)
        self.objsftp = self.obj.open_sftp()

    def getTarPackage(self):
        remotepath =self.jmeterServer.path
        packageName = self.reportName
        #压缩成tar.gz文件
        stdin,stdout,stderr  = self.obj.exec_command("cd " + remotepath +";"
                                                     + "tar -zvcf /tmp/" + packageName
                                                     + ".tar.gz " + packageName)
        msg = stdout.read().decode()
        msgQueue.put(msg)
        print(stderr.read().decode())
        # fileName =
        self.objsftp.get("/tmp/" + packageName + ".tar.gz", "../report/" + packageName + ".tar.gz")
        msg = stdout.read().decode()
        msgQueue.put(msg)
        print(stderr.read().decode())
        self.objsftp.remove("/tmp/" + packageName + ".tar.gz")
        self.objsftp.remove(remotepath+packageName+".jtl")
        # self.objsftp.remove(remotepath+packageName)
        # self.objsftp.rmdir(remotepath+packageName)
        msgQueue.put("get package from " + packageName + " ok......")

    def close(self):
        self.obj.close()

    def run(self):
        self.getTarPackage()
        self.close()

if __name__ == "__main__":
    host = "10.15.107.189"
    username = "root"
    password = "znzyjwqqlsjrghwy189"
    path = "/opt/apache-jmeter-3.2/bin/"
    jmeterServer = JmeterServer(host,username,password,path)
    t = FetchReportThread(jmeterServer,"concept_100","concept_100Thread")
    t.start()
    while True:
        print(msgQueue.get())


