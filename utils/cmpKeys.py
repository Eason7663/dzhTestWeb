#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     cmp
   Description :
   Author :       Eason
   date：          2018/3/19
-------------------------------------------------
   Change Activity:
                   2018/3/19:
-------------------------------------------------
"""
import requests
import json

class CmpKeys():
    resultList = set()

    def __init__(self,expected='',real=''):
        self.expected = expected
        self.expectedKey = set()
        self.real = real
        self.realkey = set()

        self.__resultList = set()
        self.isDifference = None
        self.diffSet = set()

    def getResult(self):
        return self.__resultList

    def isDiff(self):
        return self.isDifference

    def isSame(self):
        self.cmpJsonKeys()
        return not self.isDifference
    def isSameTable(self):
        self.cmpJsonTable()
        return not self.isDifference

    @staticmethod
    def getTable(jsn,result):
        def getTableHead(table, result, pre=""):
            # print table
            if isinstance(table, unicode):
                tmp = pre + '.' + str(table).encode("utf-8")
                result.add(tmp)
            if isinstance(table, dict):
                if table['head'] is not None:
                    li = table['head']
                    for value in li:
                        tmp = pre + '.head.' + value
                        result.add(tmp)
                if table['data'] is not None:
                    pre = pre + '.' + 'data.'
                    return getTableHead(table['data'], result, pre)
            if isinstance(table, list):
                pre = pre + '[]'
                for value in table:
                    # print value
                    getTableHead(value, result, pre)
        if jsn.has_key('Data'):
            if jsn['Data'] is not None:
                if jsn['Data'].has_key('JsonTbl'):
                    if jsn['Data']['JsonTbl'] is not None:
                        getTableHead(jsn['Data']['JsonTbl'],result)
                    else:
                        raise LookupError('JsonTbl is None')
                else:
                    raise LookupError('There is no JsonTbl')
            else:
                raise LookupError('Data is None')
        else:
            raise LookupError('There is no Data')


    def cmpJsonTable(self):
        CmpKeys.getTable(self.expected,self.expectedKey)
        CmpKeys.getTable(self.real,self.realkey)
        self.diffSet = self.expectedKey.difference(self.realkey)
        if len(self.diffSet) != 0:
            self.isDifference = True
        else:
            self.isDifference = False

    @staticmethod
    def getKeysDict(valDict,result, pre=''):
        for key,value in valDict.items():
            if pre is '':
                tmp = key
            else:
                tmp = (pre + '.' + key)
            # fk.class_var += 1
            #print tmp
            # print fk.class_var
                result.add(tmp)
            if isinstance(value,dict):
                CmpKeys.getKeysDict(value,result,tmp)
            else:
                if isinstance(value,list):
                    CmpKeys.getKeysList(value,result,tmp)

    @staticmethod
    def getKeysList(valList, result, pre=''):
        #获取数组倒数第一个，最新的
        jsn = valList[-1]
        if jsn != None:
            for key,value in jsn.items():
                if pre is '':
                    tmp = key
                else:
                    tmp = (pre + '[-1]' + key)
                # fk.class_var += 1
                # print tmp
                # print fk.class_var
                    result.add(tmp)
                if isinstance(value,dict):
                    CmpKeys.getKeysDict(value ,result, tmp)
                else:
                    if isinstance(value,list):
                        CmpKeys.getKeysList(value ,result, tmp)
        else:
            raise RuntimeError('List is null:' + str(valList))

    def cmpJsonKeys(self):
        CmpKeys.getKeysDict(self.expected,self.expectedKey)
        CmpKeys.getKeysDict(self.real,self.realkey)

        self.diffSet = self.expectedKey.difference(self.realkey)
        if len(self.diffSet) != 0:
            self.isDifference = True
        else:
            self.isDifference = False

    def getDiff(self):
        return self.diffSet


if __name__ == "__main__":
    r1 = requests.get("http://10.15.144.72/markettrend/index/kline?token=00000001%3A1607826853%3Ad3ebda847e7e5a69d22f31f433272135aeda60fc&obj=SH000001")
    jsn1 = r1.json()
    r2 = requests.get("http://10.15.144.72/markettrend/gegu/min?token=00000001%3A1607826853%3Ad3ebda847e7e5a69d22f31f433272135aeda60fc&obj=SH000001")
    jsn2 = r2.json()
    ck = CmpKeys(jsn1,jsn2)
    print r1.json()
    print r2.json()
    # result = set()
    # CmpKeys.getKeysDict(r.json(), result)
    # print result
    ck.cmpJsonKeys()
    print ck.getDiff()
    print "Same: " + str(ck.isSame())
    print "Difference: " + str(ck.isDiff())
    print ck.isDifference

