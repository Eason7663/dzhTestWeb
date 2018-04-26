#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     jmeterThread
   Description :
   Author :       Eason
   date：          2018/4/25
-------------------------------------------------
   Change Activity:
                   2018/4/25:
-------------------------------------------------
"""
import threading
import time,re
from queue import Queue
import paramiko
from appaction.singletonClass import JmeterServer,LocalServer
from appaction.fetchReportThread import FetchReportThread

# taskList = ["concept_100"]#,"concept_200","concept_300","concept_400"]
# msgQueue = Queue()




class jmxRunThread(threading.Thread):
    taskList = ["concept_100"]  # ,"concept_200","concept_300","concept_400"]
    msgQueue = Queue()
    def __init__(self,jmeterServer,threadName):
        threading.Thread.__init__(self,name=threadName)
        self.host = jmeterServer.host
        self.port = jmeterServer.port
        self.username = jmeterServer.username
        self.password = jmeterServer.password
        self.path = jmeterServer.path
        self.obj = paramiko.SSHClient()
        self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.obj.connect(self.host,self.port,self.username,self.password)
        self.objsftp = self.obj.open_sftp()

    def run(self):

        while True:
            if False:
                break
            s = self.taskList.pop(0)
            filePath = self.path + s
            cmd = "{path}jmeter -n -t {filePath}.jmx -l {filePath}.jtl".format(path=self.path,filePath=filePath)
            # time.sleep(s)
            # self.name = self.name
            # msg = self.name + " has sleeped " + str(s) + "s"
            # print("In " + self.name + ":" + msg)
            # msgQueue.put(msg)
            self.run_cmd(cmd)
            self.msgQueue.put("Task has been done: " + s)
        self.msgQueue.put("All Task Done")
        self.obj.close()

    def getErr(self,line):
        searchObj = re.search(r'Err:(.*)\((.*)\)', line, re.M | re.I)
        if searchObj:
            return searchObj.group(2)[:-1]
        else:
            return "Nothing found!!"

    def run_cmd(self, cmd):
        stdin, stdout, stderr = self.obj.exec_command(cmd)
        while True:
            try:
                line = stdout.readline()
                if line == '':
                    break
                if "Err:" in line:
                    #错误率达到80%立即停止
                    if float(self.getErr(line)) > 80:
                        cmd = "/opt/apache-jmeter-3.2/bin/shutdown.sh"
                        self.obj.exec_command(cmd)
                        cmd = "/opt/apache-jmeter-3.2/bin/stoptest.sh"
                        self.obj.exec_command(cmd)
                    #错误率在大于2%，本次执行依旧，但不再执行下个任务

                msg = threading.currentThread().getName() + " is running: " + line.strip()

                # msgQueue.put("****")
                self.msgQueue.put(msg)

            except IOError:
                break

        err = stderr.read()
        print(err.decode())
        # self.obj.close()
    def prepareJMX(self):

        pass


    def uploadJMX(self):
        pass






if __name__ == "__main__":
    # line = "summary + 142895 in 00:00:17 = 8463.3/s Avg:     8 Min:     0 Max:   675 Err:     0 (0.00%) Active: 100 Started:"
    host = "10.15.107.189"
    username = "root"
    password = "znzyjwqqlsjrghwy189"
    path = "/opt/apache-jmeter-3.2/bin/"
    jmeterServer = JmeterServer(host,username,password,path)
    t = jmxRunThread(jmeterServer,"JsvrThread")
    t.start()

    while True:
        msg = t.msgQueue.get()
        if "Task has been done:" in msg:
            reportName =msg.split()[-1]
            fetchReport = FetchReportThread(jmeterServer,reportName,"FetchReport")
            fetchReport.start()
            print(msg.split()[-1])
        print(msg)
        if msg == "All Task Done":
            break
