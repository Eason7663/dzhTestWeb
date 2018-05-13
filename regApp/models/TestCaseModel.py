#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: TestCaseModel.py
@time: 2018/05/05
"""

from __future__ import unicode_literals
from django.db import models
from .TestSuitModel import TestSuitModel
from .regAppBaseModel import RegAppBaseModel
import jsonfield

class TestCaseModel(RegAppBaseModel):
    test_suit = models.ForeignKey(TestSuitModel, on_delete=models.CASCADE, default='')
    is_enable = models.BooleanField(default=True,verbose_name="状态")
    url_path = models.CharField(max_length=64,verbose_name="Path",help_text="样例：/a/b 以‘/’开头")
    # url_param = models.TextField()
    url_param = jsonfield.JSONField(verbose_name="Param",blank=True,help_text="Tip：确认Josn格式有效，或者为空")
    # real_Result = models.TextField()
    real_Result = jsonfield.JSONField(verbose_name="实际结果",blank=True,help_text="Tip：确认Josn格式有效，或者为空")
    # expected_result = models.TextField()
    expected_result = jsonfield.JSONField(verbose_name="期望结果",blank=True,help_text="Tip：确认Josn格式有效，必选")
    pass_or_fail = models.BooleanField(default=None,verbose_name="执行结果")
    on_going = models.BooleanField(default=True,verbose_name="正在执行")
    url = models.URLField(default="http://127.0.0.1:8001/",verbose_name="完整URL",blank=True)

    def __str__(self):
        return self.name