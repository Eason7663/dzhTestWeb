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
import time,re,os
from queue import Queue
from functools import reduce
import paramiko
from appaction.singletonClass import JmeterServer,LocalServer
from appaction.fetchReportThread import FetchReportThread

# taskList = ["concept_100"]#,"concept_200","concept_300","concept_400"]
# msgQueue = Queue()




class JmxRunThread(threading.Thread):
    msgQueue = Queue()
    def __init__(self,jmeterServer,pfmCase,threadName):
        self.taskList = []
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
        ################
        self.scriptName = pfmCase.scriptName
        self.step = pfmCase.step
        self.count = pfmCase.count
        ################
        self.currentScript = ''


    def run(self):

        while len(self.taskList) > 0:
            self.prepareJMX()
            self.uploadJMX()
            if False:
                break
            filePath = self.path + self.currentScript.replace(".jmx","")
            cmd = "{path}jmeter -n -t {filePath}.jmx -l {filePath}.jtl".format(path=self.path,filePath=filePath)

            self.run_cmd(cmd)
            self.msgQueue.put("Task has been done: script->" + self.currentScript)
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
                    if float(self.getErr(line)) > 2:
                        cmd = "/opt/apache-jmeter-3.2/bin/shutdown.sh"
                        self.obj.exec_command(cmd)
                        cmd = "/opt/apache-jmeter-3.2/bin/stoptest.sh"
                        self.obj.exec_command(cmd)
                        self.msgQueue.put("错误率超过2%，本次压测结束！")
                        self.msgQueue.put("Task has been interrupted")
                        break
                    #错误率在大于2%，本次执行依旧，但不再执行下个任务

                msg = threading.currentThread().getName() + " is running: " + line.strip()

                # msgQueue.put("****")
                self.msgQueue.put(msg)

            except IOError:
                break

        err = stderr.read()
        print(err.decode())
        # self.obj.close()

    def initTaskList(self,):
        for i in range(0,self.count):
            self.taskList.append(i*self.step)

    def prepareJMX(self):

        localFile = "script/"+self.scriptName
        src = self.readFile(localFile)
        # print(src)
        p1 = re.compile(r'(?<=<stringProp name="ThreadGroup.num_threads">)(.*?)(?=</stringProp>)')
        #找到第一个
        list = p1.findall(src)
        if len(list) != 0:
            oldnums = int(list[0])
        else:
            raise LookupError("No Thread Nums")

        newNums = int(oldnums) + int(self.taskList.pop(0))
        newName = self.scriptName.replace(".jmx","_"+str(newNums)+".jmx")
        self.currentScript = newName
        content = re.sub(p1, str(newNums), src)
        newFileName = "tmp/"+newName

        with open(newFileName, 'w') as fw:
            fw.write(content)
            fw.close()

    def uploadJMX(self):
        locaFile = "tmp/" + self.currentScript
        remoteFile = "/opt/apache-jmeter-3.2/bin/" + self.currentScript
        self.objsftp.put(locaFile,remoteFile)

    def readFile(self,path):
        if not os.path.exists(path):
            print('path : \'' + path + '\' not find.')
            return []
        content = ''
        with open(path, 'r', encoding='gbk', errors='ignore') as fp:
            content += reduce(lambda x, y: x + y, fp)
        return content

    def prepareScript(self,loacalFile,step,nums,remotePath):
        self.remoteFileList = []
        tempList = loacalFile.split('/')
        scriptPath = "/".join(tempList[0:-1])
        scriptName = tempList[-1].replace(".jmx","")

        src = self.readFile(loacalFile)
        # print(src)
        p1 = re.compile(r'(?<=<stringProp name="ThreadGroup.num_threads">)(.*?)(?=</stringProp>)')
        #找到第一个
        list = p1.findall(src)
        if len(list) != 0:
            oldnums = int(list[0])
        else:
            raise LookupError("No Thread Nums")
        #生成新脚本
        for i in range(0,nums):
            newNums = oldnums+i*step
            content = re.sub(p1, str(newNums), src)
            newFileName = scriptPath+ "/" + scriptName + "_" + str(newNums) +".jmx"
            self.remoteFileList.append(newFileName)
            with open(newFileName, 'w') as fw:
                fw.write(content)
                fw.close()

        # for fi in self.remoteFileList:
        #     tempName = fi.split("/")[-1]
        #     remoteFile = remotePath + tempName
        #     self.jsvr.put(loacalFile,remoteFile)





if __name__ == "__main__":
    # line = "summary + 142895 in 00:00:17 = 8463.3/s Avg:     8 Min:     0 Max:   675 Err:     0 (0.00%) Active: 100 Started:"
    host = "10.15.107.189"
    username = "root"
    password = "znzyjwqqlsjrghwy189"
    path = "/opt/apache-jmeter-3.2/bin/"
    jmeterServer = JmeterServer(host,username,password,path)
    t = JmxRunThread(jmeterServer, "JsvrThread")
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
