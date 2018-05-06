#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: TestSuitViews.py
@time: 2018/05/05
"""

from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from regApp.models import TestProjectModel, TestSuitModel,TestCaseModel
from regApp.serializers import TestProjectSerializer,TestSuitSerializer,TestCaseSerializer
import json
from rest_framework import generics

@login_required
def suit_home_action(request):
    # jsmf = JmeterSvrModelForm(request.POST)
    return render(request, "regApp/testsuitHome.html")

#test suit管理页面
@login_required
def testsuit_manage(request):
    testsuits_list = TestSuitModel.objects.all()
    username = request.session.get('username', '')
    return render(request, "regApp/testsuit_manage.html", {"user": username, "testsuits":testsuits_list})

class TestSuitList(generics.ListCreateAPIView):

    serializer_class = TestSuitSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    def list(self, request, *args, **kwargs):
        username = request.session.get('username')
        queryset = TestSuitModel.objects.filter(owner=username)
        serializer = TestSuitSerializer(queryset, many=True)
        #bootstrap table初始化格式 total rows
        r = {}
        r['total'] = len(serializer.data)
        r['rows'] = serializer.data
        return Response(json.dumps(r))
