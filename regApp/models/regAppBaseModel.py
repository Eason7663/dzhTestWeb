#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: regAppBaseModel.py
@time: 2018/05/13
"""
from django.db import models
class RegAppBaseModel(models.Model):
    '''
    Base model for TestProjectModel, TestSuitModel, TestCaseModel
    '''
    #名称
    name = models.CharField(max_length=64)
    #owner
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    #描述
    description = models.CharField(max_length=256,blank=True)

    class Meta:
        abstract = True