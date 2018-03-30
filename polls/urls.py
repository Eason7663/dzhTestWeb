#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     urls
   Description :
   Author :       Eason
   date：          2018/3/28
-------------------------------------------------
   Change Activity:
                   2018/3/28:
-------------------------------------------------
"""
from django.conf.urls import url
from . import views

urlpatterns = {
    url(r'^index/', views.index, name = 'index'),
}