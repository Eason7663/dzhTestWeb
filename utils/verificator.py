#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     verificator
   Description :
   Author :       Eason
   date：          2018/4/18
-------------------------------------------------
   Change Activity:
                   2018/4/18:
-------------------------------------------------
"""
import json

def getKeysDict(valDict, result, pre=''):
    for key, value in valDict.items():
        if pre is '':
            tmp = key
            result.add(tmp)
        else:
            tmp = (pre + '.' + key)
            # fk.class_var += 1
            # print tmp
            # print fk.class_var
            result.add(tmp)
        if isinstance(value, dict):
            getKeysDict(value, result, tmp)
        elif isinstance(value, list) and len(value) >0:
                getKeysList(value, result, tmp)




def getKeysList(valList, result, pre=''):
    # 获取数组倒数第一个，最新的
    jsn = valList[-1]
    if jsn != None:
        for key, value in jsn.items():
            if pre is '':
                tmp = key
            else:
                tmp = (pre + '[-1]' + key)
                # fk.class_var += 1
                # print tmp
                # print fk.class_var
                result.add(tmp)
            if isinstance(value, dict):
                getKeysDict(value, result, tmp)
            else:
                if isinstance(value, list):
                    getKeysList(value, result, tmp)
    else:
        raise RuntimeError('List is null:' + str(valList))

class VerifyJson():
    real = {}
    realKey = set()
    expected = {}
    expectedKey = set()
    isSame = None
    expectedNotHas = set()
    realNotHas = set()

    def __init__(self,real,expected):
        self.real=real
        self.expected=expected
        self.cmpJsonKeys()

    def cmpJsonKeys(self):
        getKeysDict(self.expected,self.expectedKey)
        getKeysDict(self.real,self.realKey)

        self.expectedNotHas = self.expectedKey.difference(self.realKey)
        self.realNotHas = self.realKey.difference(self.expectedKey)
        print("self.expectedNotHas = " + str(self.expectedNotHas))
        print("self.realNotHas = "+ str(self.realNotHas))
        if len(self.expectedNotHas) == 0 and len(self.realNotHas) == 0:
            self.isSame = True
        else:
            self.isSame = False
        self.expectedKey.clear()
        self.realKey.clear()


if __name__ == "__main__":

    jsn1 = {"aa":"1","bb":2,"cc":3}
    jsn2 = {"bb":"1","cc":2,"ee":1}

    print(VerifyJson(jsn1,jsn2).isSame)
