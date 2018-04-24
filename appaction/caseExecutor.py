#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: caseExecutor.py
@time: 2018/04/15
"""
# import os
# os.environ.update({"DJANGO_SETTINGS_MODULE": "TestFrameWork.settings"
import requests
from utils.verificator import VerifyJson

class caseExecutor():
    def __init__(self,config,testCase):
        self.testCase = testCase
        self.config = config

    def getYunToken(self):
        path = "/token/access"
        url = self.config['protocol'] + self.config['host'] + path
        keys = {'appid', 'secret_key'}
        param = {key: value for key, value in self.config.items() if key in keys}
        response = requests.get(url, params=param)
        print(response.url)
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
        param= self.testCase.url_param
        print(param)
        # print(self.getYunToken())
        if isinstance(param,str):
            return self.getYunToken()
        else:
            tmp= {**param,**self.getYunToken()}
            return tmp

    def executor(self):
        # 指定params参数
        response = requests.get(self.getURL(),params=self.getParam())
        # response = requests.get(self.getURL())
        #
        expected = self.testCase.expected_result
        # print(type(expected))
        # if isinstance(expected, str):  # 首先判断变量是否为字符串
        #     try:
        #         json.loads(expected)
        #     except ValueError:
        #         print("False1")
        #     print("True")
        # else:
        #     print("False2")
        # print(expected)
        real = response.json()
        ck = VerifyJson(expected,real)
        self.testCase.pass_or_fail = ck.isSame
        self.testCase.real_Result = real
        self.testCase.url = response.url
        self.testCase.save()
        # print(response.url)
        # print(self.getParam())

