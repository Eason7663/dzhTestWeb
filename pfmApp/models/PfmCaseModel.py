#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     PfmCaseModel
   Description :
   Author :       Eason
   date：          2018/5/3
-------------------------------------------------
   Change Activity:
                   2018/5/3:
-------------------------------------------------
"""

from django.db import models

class PfmCaseModel(models.Model):
    name = models.CharField(verbose_name="用例名称",max_length=64)
    scriptName = models.CharField(verbose_name="脚本名称",max_length=64)
    step = models.IntegerField(verbose_name="单次增加的线程数",)
    count = models.IntegerField(verbose_name="计划执行次数",)
    class Meta:
        app_label = 'pfmApp'
        ordering = ('id',)

    def __str__(self):
        return self.name

class SubPfmCaseModel(models.Model):
    pfmCase = models.ForeignKey(PfmCaseModel, on_delete=models.CASCADE,)
    name = models.CharField(verbose_name="用例名称",max_length=64)
    scriptName = models.CharField(verbose_name="脚本名称",max_length=64)
    threadNums = models.IntegerField(verbose_name="当前线程数")
    class Meta:
        app_label = 'pfmApp'
        ordering = ('id',)