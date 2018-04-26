#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     performanceApp
   Description :
   Author :       Eason
   date：          2018/4/23
-------------------------------------------------
   Change Activity:
                   2018/4/23:
-------------------------------------------------
"""
import os,re
from functools import reduce
from appaction.jServer import JmeterServer

class PerformanceApp():
    def __init__(self,hostip,username,password,path):
        self.path = path
        self.jsvr = JmeterServer(hostip,username,password)
        self.remoteFileList =[]

    def lanuchServer(self):

        for jmxFile in self.remoteFileList:
            filePath = self.path + jmxFile.split('/')[-1].replace(".jmx","")
            cmd = "{path}jmeter -n -t {filePath}.jmx -l {filePath}.jtl -e -o {filePath}".format(path=self.path,filePath=filePath)
            self.jsvr.run_cmd(cmd)

    def getReport(self,path,jmxname):
        self.jsvr.getTarPackage(path,jmxname)

    def close(self):
        self.jsvr.close()

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

        for fi in self.remoteFileList:
            tempName = fi.split("/")[-1]
            remoteFile = remotePath + tempName
            self.jsvr.put(loacalFile,remoteFile)

    def getReportNameList(self):
        tmpList = []
        for tmp in self.remoteFileList:
            tmpList.append(tmp.split("/")[-1].replace(".jmx",""))
        return tmpList



if __name__ == "__main__":
    remotePath = "/opt/apache-jmeter-3.2/bin/"
    host = "10.15.107.189"
    username = "root"
    pasword = "znzyjwqqlsjrghwy189"
    # jmxname = "concept"
    pf = PerformanceApp("10.15.107.189","root","znzyjwqqlsjrghwy189",remotePath)
    # # pf.lanuchServer(path,jmxname)
    # pf.getReport(path,jmxname)
    # print(path.split('/')[0:-1])
    script = "../tmp/concept.jmx"
    pf.prepareScript(script,100,4,remotePath)
    print(pf.remoteFileList)
    pf.lanuchServer()
    for reportName in pf.getReportNameList():
        pf.getReport(remotePath,reportName)

    pf.close()
