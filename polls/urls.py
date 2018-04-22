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
from . import views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'project',views.TestProject)
router.register(r'cases',views.TestCaseViewSet)



urlpatterns = [
    url(r'^testproject/$', views.TestProjectList.as_view()),
    url(r'^testproject/(?P<pk>[0-9]+)/$', views.TestProjectDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^$', views.index, name = 'index'),
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
]