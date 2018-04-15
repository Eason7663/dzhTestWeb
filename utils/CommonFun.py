#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     GetYunToken
   Description :
   Author :       Eason
   date：          2018/3/20
-------------------------------------------------
   Change Activity:
                   2018/3/20:
-------------------------------------------------
"""
from constant.config import *
import requests
import json
from utils.cmpKeys import CmpKeys

#获取云平台token
def GetYunToken():
    keys = {'appid', 'secret_key'}
    paramfortoken = {key: value for key, value in yunconsole_config.items() if key in keys}
    url = yunconsole_config['protocol'] + yunconsole_config['ip'] + '/token/access'
    r = requests.get(url, paramfortoken)
    yuntoken = r.json()['Data']['RepDataToken'][0]['token']
    return yuntoken

def GetJsonReponse(path, param):
    #需要完善返回
    url = yunconsole_config['protocol'] + yunconsole_config['ip'] + path
    parambase = {"token": GetYunToken()}
    parambase.update(param)
    r = requests.get(url,parambase)
    # print r.url
    if r.status_code == 200:
        return r.json()

def GetExpectedJson(filePath):
    with open(filePath,'r') as load_f:
        return json.load(load_f)

def CompareJson(expected,real):
    ck = CmpKeys(expected,real)
    return ck.isSame()

def CompareJsonTable(expected,real):
    ck = CmpKeys(expected,real)
    return ck.isSameTable()

if __name__ == "__main__":
    print(GetYunToken())

