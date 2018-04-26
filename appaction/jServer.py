#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     jmeterServer
   Description :
   Author :       Eason
   date：          2018/4/23
-------------------------------------------------
   Change Activity:
                   2018/4/23:
-------------------------------------------------
"""

import paramiko

class JmeterServer:
    def __init__(self,hostip="",username="",password="",port=22):
        self.hostip = hostip
        self.port = port
        self.username = username
        self.password = password
        self.obj = paramiko.SSHClient()
        self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.obj.connect(self.hostip,self.port,self.username,self.password)
        self.objsftp = self.obj.open_sftp()

    def run_cmd(self,cmd):
        stdin,stdout,stderr = self.obj.exec_command(cmd)
        while True:
            try:
                line = stdout.readline()
                if line == '':
                    break
                print("line" + line)
            except IOError:
                break

        err = stderr.read()
        print(err.decode())

    def run_cmdlist(self,cmdlist):
        self.resultList = []
        for cmd in cmdlist:
            stdin,stdout,stderr = self.obj.exec_command(cmd)
            self.resultList.append(stdout.read())
        return self.resultList

    def get(self,remotepath,localpath):
        self.objsftp.get(remotepath,localpath)

    def put(self,localpath,remotepath):
        self.objsftp.put(localpath,remotepath)

    def getTarPackage(self,remotepath,dirname):
        packageName = dirname
        #压缩成tar.gz文件
        stdin,stdout,stderr  = self.obj.exec_command("cd " + remotepath +";"
                                                     + "tar -zvcf /tmp/" + packageName
                                                     + ".tar.gz " + packageName)
        print(stdout.read().decode())
        print(stderr.read().decode())

        # fileName =
        self.objsftp.get("/tmp/" + packageName + ".tar.gz", "../tmp/"+packageName + ".tar.gz")
        self.objsftp.remove("/tmp/" + packageName + ".tar.gz")
        print("get package from " + packageName + " ok......")

    def close(self):
        self.objsftp.close()
        self.obj.close()

import tarfile
import gzip
def unGz(file):
    """ungz zip file"""
    f_name = file.replace(".gz", "")
    #获取文件的名称，去掉
    g_file = gzip.GzipFile(file)
    #创建gzip对象
    open(f_name, "wb+").write(g_file.read())
    #gzip对象用read()打开后，写入open()建立的文件里。
    g_file.close()
    #关闭gzip对象

import os
def unTar(file):
    """untar zip file"""
    tar = tarfile.open(file)
    names = tar.getnames()
    if os.path.isdir(file + "_files"):
        pass
    else:
        os.mkdir(file + "_files")
    #因为解压后是很多文件，预先建立同名目录
    for name in names:
        tar.extract(name, file + "_files/")
    tar.close()

if __name__ == '__main__':
    sshobj = JmeterServer('10.15.107.189','root','znzyjwqqlsjrghwy189',22)
    # sshobj.getTarPackage("/opt/apache-jmeter-3.2/bin/","rr")
    # sshobj.close()
    # unGz("rr.tar.gz")
    # unTar("rr.tar")
    sshobj.put("../tmp/concept_100.jmx","/opt/concept_100.jmx")