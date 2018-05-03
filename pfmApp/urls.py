#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: urls.py
@time: 2018/04/29
"""

from django.conf.urls import url
from pfmApp.view import pfmCaseView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# router.register(r'jmx_analyze/', views.testTable)

urlpatterns = [
    url(r'^jmx/analyze/$', pfmCaseView.testTable, name="jmx_analyze"),
    url(r'pfmCase/home$', pfmCaseView.testTable),
    url(r'execute/case/(?P<case_id>[0-9]+)', pfmCaseView.execute_pfmCase)
]