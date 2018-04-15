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

    def getURL(self):
        url = self.config['protocol'] + self.config['host'] + self.testCase.url_path
        return url
    def getParam(self):
        return self.testCase.url_param

    def executor(self):
        # print(json.loads(self.getParam()))
        response = requests.get(self.getURL(),json.loads(self.getParam()))
        expected = json.loads(self.testCase.expected_result)
        real = response.json()
        ck = CmpKeys(expected,real)
        ck.cmpJsonKeys()
        self.testCase.pass_or_fail= ck.isSame()
        self.testCase.real_Result=real
        self.testCase.url = response.url
        self.testCase.save()
        # print(response.url)

