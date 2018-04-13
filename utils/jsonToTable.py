#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     jsonToTable
   Description :
   Author :       Eason
   date：          2018/3/22
-------------------------------------------------
   Change Activity:
                   2018/3/22:
-------------------------------------------------
"""

from json2table import convert
import requests
from json2html import *
reload(sys)
sys.setdefaultencoding('utf-8')
from utils.cmpKeys import CmpKeys

def getTableHead(table,result,pre = ""):
    # print table
    if isinstance(table,unicode):
        tmp = pre + '.' + str(table).encode("utf-8")
        result.append(tmp)
    if isinstance(table,dict):
        if table['head'] is not None:
            li = table['head']
            for value in li:
                tmp = pre + '.head.' + value
                result.append(tmp)
        if table['data'] is not None:
            pre = pre + '.' + 'data.'
            return getTableHead(table['data'], result, pre)
    if isinstance(table,list):
        pre = pre + '[]'
        for value in table:
            # print value
            getTableHead(value, result, pre)



if __name__ == "__main__":
    url = "http://10.15.144.72/markettrend/topicinvest?token=00000001%3A1607826853%3Ad3ebda847e7e5a69d22f31f433272135aeda60fc&obj=SH600000"
    r = requests.get(url)
    r2 = requests.get("http://10.15.144.72/markettrend/gegu/min?token=00000001%3A1607826853%3Ad3ebda847e7e5a69d22f31f433272135aeda60fc&obj=SH000001")
    jsn2 = r2.json()
    # print r.json()
    # json_object = r.json()
    # build_direction = "LEFT_TO_RIGHT"
    # table_attributes = {"style": "width:100%"}
    # html = convert(json_object, build_direction=build_direction, table_attributes=table_attributes)
    # with open('rrr.html','wb') as f:
    #     f.write(html)
    # print html
    # infoFromJson = r.json()
    # print json2html.convert(json=infoFromJson)
    # with open('rrr2.html','wb') as f:
    #     f.write(json2html.convert(json=infoFromJson))
    # jt =  r.json()['Data']['JsonTbl']
    # result = []
    #
    # getTableHead(jt,result)
    #
    # print "result : " + str(result)

    ck = CmpKeys(r.json(),r.json())
    ck.cmpJsonTable()
    print ck.isSameTable()

