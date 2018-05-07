#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: TestProjectViews.py
@time: 2018/05/05
"""
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from regApp.models import TestProjectModel, TestSuitModel,TestCaseModel
from regApp.serializers import TestProjectSerializer,TestSuitSerializer,TestCaseSerializer
from rest_framework import generics
from rest_framework import permissions
from regApp.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@login_required
def project_home_action(request):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # jsmf = JmeterSvrModelForm(request.POST)
    return render(request, "regApp/testprojectHome.html")

@login_required
def add_project_action(request):
    print(request.POST)
    tp = TestProjectModel()
    tp.name = request.POST.get('name')
    tp.is_enable = True
    #当前用户即为创建者
    user = request.user
    # print(user)
    tp.owner = user
    tp.description = request.POST.get('description')
    tp.create_time = request.POST.get('create_time')
    # if tp.is_valid():
    try:
        tp.save()
    except BaseException:
        print("error")
    return JsonResponse({"A":"B"})

#test project管理页面
@login_required
def testproject_manage(request):
    username = request.session.get('username', '')
    testprojects_list = TestProjectModel.objects.filter(owner=username)
    return render(request, "regApp/testproject_manage.html", {"user": username, "testprojects":testprojects_list})


from django.contrib.auth import get_user_model

User = get_user_model()

class TestProjectList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TestProjectSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    def list(self, request, *args, **kwargs):
        username = request.session.get('username')
        owner = User.objects.get(username=username)

        # print(owner.id)
        queryset = TestProjectModel.objects.filter(owner=owner.id)
        serializer = TestProjectSerializer(queryset, many=True)
        #bootstrap table初始化格式 total rows
        r = {
            "total":len(serializer.data),
            "rows":serializer.data
        }
        return JsonResponse(r)

class TestProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestProjectModel.objects.all()
    serializer_class = TestProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)