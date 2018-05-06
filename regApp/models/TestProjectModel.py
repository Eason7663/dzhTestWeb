#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: TestProjectModel.py
@time: 2018/05/05
"""

from __future__ import unicode_literals
from django.db import models

# Create your models here.
class TestProjectModel(models.Model):
    #主键 project_id
    #id 主键， by default, django gives each model the field named id (id = models.AutoField(primary_key=True))
    # 名称
    name = models.CharField(max_length=64)
    is_enable = models.BooleanField(default=True)
    suit_number = models.BigIntegerField(default=0,null=True)
    last_modified = models.DateTimeField(auto_now=True,null=True)
    # owner
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    #描述
    description = models.CharField(max_length=256)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        representation of the code snippet.
        """
        super(TestProjectModel, self).save(*args, **kwargs)