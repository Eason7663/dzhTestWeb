#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: TestCaseViews.py
@time: 2018/05/05
"""
#创建TestCase视图集
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from django.http import HttpResponse
from regApp.models import TestProjectModel, TestSuitModel,TestCaseModel
from regApp.serializers import TestProjectSerializer,TestSuitSerializer,TestCaseSerializer
from regApp.forms import TestProjectForm,TestSuitForm,TestCaseForm
from conf import constConf
from appaction.caseExecutor import caseExecutor
from rest_framework import generics

@login_required
def case_home_action(request):
    # jsmf = JmeterSvrModelForm(request.POST)
    return render(request, "regApp/testcaseHome.html")

@login_required
def add_case_action(request):
    tcf = TestCaseForm(request.POST)
    return render(request, "regApp/testcase_add2.html", {'form':tcf})

#test case管理页面
@login_required
def testcase_manage(request):
    testcases_list = TestCaseModel.objects.all()
    username = request.session.get('username', '')
    return render(request, "regApp/testcase_manage.html", {"user": username, "testcases":testcases_list})

@login_required
def add_post_case_action(request):
    # if request
    tcf = TestCaseForm(request.POST)
    if tcf.is_valid():
        # print(tcf)
        tcf.save()
        return HttpResponse("hello")
    return Response(tcf)

# class TestCaseViewSet(viewsets.ReadOnlyModelViewSet):
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,IsAuthenticatedOrReadOnly)
#     def get_object(self):
#         print("hello")
#         obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
#         self.check_object_permissions(self.request, obj)
#         return obj
#     """API endpoint for listing test cases."""
#     queryset = TestCaseModel.objects.all()
#     serializer_class = TestCaseSerializer
#     # def perform_create(self,serializer):
#     #     print(self.request.user)
#     #     serializer.save(owner=User.objects.get(id=self.request.session.get('username')))
#     def get(self, request, *args, **kwargs):
#         print(request.user)
#         return Response("hello")
#     def list(self, request, *args, **kwargs):
#         print(request.session.get("username"))
#         queryset = TestCaseModel.objects.filter(test_suit__owner=request.session.get("username"))
#         # queryset = TestCase.objects.all()
#         serializer = TestCaseSerializer(queryset, many=True)
#         return Response(serializer.data)


class TestCaseList(generics.ListCreateAPIView):

    serializer_class = TestCaseSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    def list(self, request, *args, **kwargs):
        username = request.session.get('username')
        queryset = TestCaseModel.objects.filter(owner=username)
        serializer = TestCaseSerializer(queryset, many=True)
        #bootstrap table初始化格式 total rows
        r = {}
        r['total'] = len(serializer.data)
        r['rows'] = serializer.data
        # return Response(json.dumps(r))
        return Response(r)


def execute_case_action(request,case_id):
    testCase = TestCaseModel.objects.get(id=case_id)
    ce = caseExecutor(constConf.yunconsole_config,testCase)
    ce.executor()
    return HttpResponse(testCase.pass_or_fail)

#返回单个用例执行结果
def execute_case_detail_action(request,case_id):
    testCase = TestCaseModel.objects.get(id=case_id)
    response = {}
    response['url'] = testCase.url
    response['result'] = testCase.real_Result
    return JsonResponse(response)