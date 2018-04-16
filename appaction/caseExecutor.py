#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: caseExecutor.py
@time: 2018/04/15
"""
# import os
# os.environ.update({"DJANGO_SETTINGS_MODULE": "TestFrameWork.settings"
from django.test.testcases import *
from polls.models import TestCase
from conf.constConf import yunconsole_config
from utils.cmpKeys import CmpKeys
import json
import requests

class caseExecutor():
    def __init__(self,config,testCase):
        self.testCase = testCase
        self.config = config

    def getYunToken(self):
        path = "/token/access"
        url = self.config['protocol'] + self.config['host'] + path
        keys = {'appid', 'secret_key'}
        param = {key: value for key, value in self.config.items() if key in keys}
        response = requests.get(url, param)
        yunToken = response.json()['Data']['RepDataToken'][0]['token']
        # pattern = re.compile('token')
        # yunToken = pattern.match(response.text)
        # print(yunToken)
        # print(response.text)
        result = {}
        result["token"]=yunToken
        return result

    def getURL(self):
        url = self.config['protocol'] + self.config['host'] + self.testCase.url_path
        return url
    def getParam(self):
        param= json.loads(self.testCase.url_param)
        print(self.getYunToken())
        tmp= {**param,**self.getYunToken()}
        return tmp

    def executor(self):
        # # print(json.loads(self.getParam()))
        response = requests.get(self.getURL(),self.getParam())
        expected = json.loads(self.testCase.expected_result)
        real = response.json()
        ck = CmpKeys(expected,real)
        ck.cmpJsonKeys()
        self.testCase.pass_or_fail= ck.isSame()
        self.testCase.real_Result=real
        self.testCase.url = response.url
        self.testCase.save()
        # print(response.url)
        # print(self.getParam())

