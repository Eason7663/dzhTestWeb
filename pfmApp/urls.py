#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: urls.py
@time: 2018/04/29
"""

from django.conf.urls import url,include
from . import views
from rest_framework.routers import DefaultRouter,SimpleRouter

router = SimpleRouter()
# router.register(r'jmx_analyze/', views.testTable)

urlpatterns = [
    url(r'^jmx/analyze/$', views.testTable,name="jmx_analyze"),
    url(r'pfmCase/home$',views.testTable)
]