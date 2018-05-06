#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: TestSuitModel.py
@time: 2018/05/05
"""

from __future__ import unicode_literals
from django.db import models
from .TestProjectModel import TestProjectModel


class TestSuitModel(models.Model):
    test_project = models.ForeignKey(TestProjectModel, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=64)
    is_enable = models.BooleanField(default=True)
    case_number = models.BigIntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.CharField(max_length=64)
    pass_case = models.IntegerField()
    fail_case = models.IntegerField()
    #描述
    description = models.CharField(max_length=256)
    on_going = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name