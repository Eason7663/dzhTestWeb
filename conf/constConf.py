#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: constConf.py
@time: 2018/04/15
"""
import requests
import re
yunconsole_config = {
    "protocol":"http://",
    "host":"gw.yundzh.com",
    "appid":"ab1c4cf2466e11e78e710242ac110008",
    "secret_key":"dIqKXbLNPV8A"
}
# yunconsole_config = {
#     "protocol":"http://",
#     "host":"10.15.144.72",
#     "appid":"e823f5e07d7311e694b60242ac11000a",
#     "secret_key":"3J0tXPi2jmrS"
# }

def getYunToken():
    path = "/token/access"
    url = yunconsole_config['protocol'] + yunconsole_config['host'] + path
    keys = {'appid','secret_key'}
    param = { key:value for key,value in yunconsole_config.items() if key in keys}
    response = requests.get(url,param)
    yunToken = response.json()['Data']['RepDataToken'][0]['token']
    # pattern = re.compile('token')
    # yunToken = pattern.match(response.text)
    # print(yunToken)
    # print(response.text)
    return yunToken