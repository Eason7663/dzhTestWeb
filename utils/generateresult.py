#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     generateresult
   Description :
   Author :       Eason
   date：          2018/3/16
-------------------------------------------------
   Change Activity:
                   2018/3/16:
-------------------------------------------------
"""

import requests

if __name__ == "__main__":
    resultpath = "../testcases/markettrend/" + "MarkettrendTopic.json"
    url = "http://10.15.144.72/markettrend/topicinvest?token=00000001%3A1607826853%3Ad3ebda847e7e5a69d22f31f433272135aeda60fc"
    r = requests.get(url)
    with open(resultpath,'w') as fi:
        fi.write(r.text.encode('utf-8'))