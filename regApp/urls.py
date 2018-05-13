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
from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
from .views import TestProjectViews,TestSuitViews,TestCaseViews,UserViews

router = DefaultRouter()
# router.register(r'project',views.TestProject)
# router.register(r'cases',views.TestCaseViewSet)



urlpatterns = [
    ###################返回创建bootstrap table所需的json list
    url(r'^testproject/$', TestProjectViews.TestProjectList.as_view()),
    url(r'^testproject/(?P<pk>[0-9]+)/$', TestProjectViews.TestProjectDetail.as_view()),
    url(r'^testsuit$', TestSuitViews.TestSuitList.as_view()),
    url(r'^testcase$', TestCaseViews.TestCaseList.as_view()),

    url(r'^users/$', UserViews.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserViews.UserDetail.as_view()),
    # url(r'^$', UserViews.index, name = 'index'),
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    url(r'^testproject/add',TestProjectViews.add_project_action),
    ###################主页请求
    url(r'project/home$', TestProjectViews.project_home_action,name='project_home'),
    url(r'suit/home$', TestSuitViews.suit_home_action,name='suit_home'),
    url(r'case/home$', TestCaseViews.case_home_action,name='case_home'),
    ###################执行case
    url(r'execute_case/(?P<case_id>[0-9]+)/$', TestCaseViews.execute_case_action),
    url(r'execute_case/detail/(?P<case_id>[0-9]+)/$', TestCaseViews.execute_case_detail_action),
]