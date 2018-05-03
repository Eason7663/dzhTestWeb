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
import os
import tarfile
from queue import Queue
# msgQueue = Queue()

class JmeterServer():
    def __init__(self,host,username,password,path,port=22):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.path = path

class FetchReportThread(threading.Thread):
    def __init__(self,jmeterServer,reportName,msgQueue,threadName):
        threading.Thread.__init__(self,name=threadName)
        self.jmeterServer =jmeterServer
        self.reportName =reportName
        self.host = jmeterServer.host
        self.port = jmeterServer.port
        self.username = jmeterServer.username
        self.password = jmeterServer.password
        self.path = jmeterServer.path
        self.obj = paramiko.SSHClient()
        self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.obj.connect(self.host,self.port,self.username,self.password)
        self.objsftp = self.obj.open_sftp()
        self.msgQueue = msgQueue

    def getTarPackage(self):
        remotepath =self.jmeterServer.path
        packageName = self.reportName
        #压缩成tar.gz文件
        stdin,stdout,stderr  = self.obj.exec_command("cd " + remotepath +";"
                                                     + "tar -zvcf /tmp/" + packageName
                                                     + ".tar.gz " + packageName)
        msg = stdout.read().decode()
        self.msgQueue.put(msg)
        print(stderr.read().decode())
        # fileName =
        self.objsftp.get("/tmp/" + packageName + ".tar.gz", "report/" + packageName + ".tar.gz")
        msg = stdout.read().decode()
        self.msgQueue.put(msg)
        print(stderr.read().decode())
        self.objsftp.remove("/tmp/" + packageName + ".tar.gz")
        self.objsftp.remove(remotepath+packageName)
        # self.objsftp.remove(remotepath+packageName)
        # self.objsftp.rmdir(remotepath+packageName)
        self.msgQueue.put("get package from " +remotepath+ packageName + " ok......")

    def unTar(self,desFilePath):
        """untar zip file"""
        file = 'report/'+ self.reportName+".tar.gz"
        tar = tarfile.open(file)
        names = tar.getnames()
        if os.path.isdir(desFilePath):
            pass
        else:
            os.mkdir(desFilePath)
        # 因为解压后是很多文件，预先建立同名目录
        for name in names:
            # tar.extract(name, file + "_files/")
            tar.extract(name, desFilePath)
        tar.close()

    def jtl2Html(self,path):
        cmd = "{path}\\"+"jmeter -g " + "{path}\\"+self.reportName + "-e -o " + "{path}\\"+self.reportName.replace(".jtl","").format(path=path)
        print(cmd)
        mystr = os.popen(cmd)
        mystr = mystr.read()  # 读取输出
        print("hello", mystr)

    def close(self):
        self.obj.close()

    def run(self):
        self.getTarPackage()
        self.unTar("D:\\0DevelopTool\\apache-jmeter-3.2\\bin")
        self.jtl2Html("D:\\0DevelopTool\\apache-jmeter-3.2\\bin")
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
        print(t.msgQueue.get())


