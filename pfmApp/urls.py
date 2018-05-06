#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: urls.py
@time: 2018/04/29
"""

from django.conf.urls import url
from pfmApp.view import pfmCaseView,websocketSvrView,ExampleView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# router.register(r'jmx_analyze/', views.testTable)

urlpatterns = [
    url(r'^jmx/analyze/$', pfmCaseView.pfmCase_home_view, name="jmx_analyze"),
    url(r'pfmCase/home$', pfmCaseView.pfmCase_home_view),
    url(r'execute/case/(?P<case_id>[0-9]+)', pfmCaseView.execute_pfmCase),
    url(r'webClient', websocketSvrView.echo),
    url(r'example/get',ExampleView.ExampleView.as_view()),
    url(r'customAuthToken/get',ExampleView.CustomAuthToken.as_view()),
    url(r'^performance/case/add$', pfmCaseView.add_jmeter_server_action),
    url(r'^pfmApp/script/upload$', pfmCaseView.script_upload_action),
    url(r'^jmx/analyze/page$', pfmCaseView.pfmCase_home_view),
]