#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     performanceTest
   Description :
   Author :       Eason
   date：          2018/4/21
-------------------------------------------------
   Change Activity:
                   2018/4/21:
-------------------------------------------------
"""
import re
import os
import bs4
import lxml
import paramiko
from xml.dom.minidom import parse
import xml.dom.minidom
from xml.etree.ElementTree import ElementTree,Element
from functools import reduce

LABEL_PATTERN = re.compile('(<(?P<label>\S+)>.+?</(?P=label)>)')
LABEL_CONTENT_PATTERN = re.compile('<(?P<label>\S+)>(.*?)</(?P=label)>')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filePath = "{}\\tmp\\concept.jmx".format(BASE_DIR)

def readFile(path):
    if not os.path.exists(path):
        print('path : \''+ path + '\' not find.')
        return []
    content =''
    with open(path, 'r', encoding='gbk', errors='ignore') as fp:
        content += reduce(lambda x, y: x + y, fp)
    return content

def modifyScript(path,nums):

    src = readFile(path)
    # print(src)
    p1 = re.compile(r'(?<=<stringProp name="ThreadGroup.num_threads">)(.*?)(?=</stringProp>)')
    print(p1.findall(src))
    content = re.sub(p1,nums,src)
    print(content)
    with open("new.jmx",'w') as fw:
        fw.write(content)

def lanchServer():
    #创建SSH对象
    ssh = paramiko.SSHClient()
    #允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #连接服务器
    ssh.connect(hostname='10.15.107.189', port=22, username='root', password='znzyjwqqlsjrghwy189')
    #执行命令
    command = "{path}jmeter -n -t {path}concept.jmx -l {path}concept.jtl -e -o {path}rr >test.log 2>&1".format(path="/opt/apache-jmeter-3.2/bin/")
    print(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    print("over1")
    result = stdout.read()
    print(result.decode())
    ssh.close()

if __name__ == "__main__":


    # modifyScript(filePath,'300')
    lanchServer()