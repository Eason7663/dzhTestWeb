from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


from polls.models import TestProject, TestSuit,TestCase
from polls.serializers import TestProjectSerializer
from polls.forms import TestCaseForm
from polls.permissions import IsOwnerOrReadOnly


import time
@login_required
def add_case_action(request):
    tcf = TestCaseForm(request.POST)
    return render(request,"polls/testcase_add2.html",{'form':tcf})

from django.forms import Form
# @csrf_exempt
@login_required
def add_post_case_action(request):
    # if request
    tcf = TestCaseForm(request.POST)
    if tcf.is_valid():
        # print(tcf)
        tcf.save()
        return HttpResponse("hello")
    return Response(tcf)
    # else:
        # return render(request, "polls/testcase.html", {'form': tcf})


# 首页(登录)
def index(request):
    return render(request, "polls/index.html")


# 登录动作
@csrf_protect
def login_action(request):
    if request.method == "POST":
        # 寻找名为 "username"和"password"的POST参数，而且如果参数没有提交，返回一个空的字符串。
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        if username == '' or password == '':
            return render(request,"polls/index.html",{"error":"username or password null!"})

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user) # 验证登录
            response = HttpResponseRedirect('/testproject_manage/') # 登录成功跳转home页面
            request.session['username'] = username    # 将 session 信息写到服务器
            return response
            # return HttpResponse('HELLO')
        else:
            return render(request,"polls/index.html",{"error":"username or password error!"})
    # 防止直接通过浏览器访问 /login_action/ 地址。
    return render(request,"index.html")

@login_required
def logout_action(request):
    auth.logout(request)
    return render(request, "polls/index.html")

#test project管理页面
@login_required
def testproject_manage(request):
    username = request.session.get('username', '')
    testprojects_list = TestProject.objects.filter(owner=username)
    return render(request, "polls/testproject_manage.html", {"user": username,"testprojects":testprojects_list})

#test suit管理页面
@login_required
def testsuit_manage(request):
    testsuits_list = TestSuit.objects.all()
    username = request.session.get('username', '')
    return render(request, "polls/testsuit_manage.html", {"user": username,"testsuits":testsuits_list})

#test case管理页面
@login_required
def testcase_manage(request):
    testcases_list = TestCase.objects.all()
    username = request.session.get('username', '')
    return render(request, "polls/testcase_manage.html", {"user": username,"testcases":testcases_list})

# project name 搜索
@login_required
def search_project_name(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name.encode(encoding="utf-8")
    testprojects_list = TestProject.objects.filter(name__contains=search_name_bytes)
    return render(request, "polls/testproject_manage.html", {"user": username, "testprojects": testprojects_list})

# help文档
@login_required
def help_document(request):
    return HttpResponse("Preparing!")
    # detect if args is well-format

    # try:
    #     article_id = int(args)
    # except:
    #     return HttpResponse("Invalid Article Number...")
    #
    # article_list = Article.objects.all()
    # if article_id not in range(1, len(article_list) + 1):
    #     return HttpResponse("Invalid Article Number...")
    #
    # atc = Article.objects.get(id=article_id)
    # template = loader.get_template('show_atc.html')
    #
    # # show markdown text
    # mfile = open('./../../django-markdown-deux.md', 'r').read()
    # atc.content = mfile
    #
    # return_dict = {'title': atc.title, 'category': atc.category, 'date': atc.date_time, 'content': atc.content}
    # return HttpResponse(template.render(return_dict, request))


from conf import constConf
from appaction.caseExecutor import caseExecutor
# 执行用例
def execute_case_action(request,case_id):
    # time.sleep(1)
    testCase = TestCase.objects.get(id=case_id)
    ce = caseExecutor(constConf.yunconsole_config,testCase)
    ce.executor()
    return HttpResponse(testCase.pass_or_fail)
#返回单个用例执行结果
def execute_case_detail_action(request,case_id):
    testCase = TestCase.objects.get(id=case_id)
    response = {}
    response['url'] = testCase.url
    response['result'] = testCase.real_Result
    return JsonResponse(response)


# #返回json格式test project
# @api_view(['GET','POST'])
# def testProject_list(request):
#     """
#     List all testproject, or create a new testproject.
#     :param request:
#     :return:
#     """
#     if request.method == 'GET':
#         testProject = TestProject.objects.all()
#         serializer = TestProjectSerializer(testProject,many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = TestProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # serializer.data 数据创建成功后所有数据
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         # serializer.errors 错误信息
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET','POST'])
# def testProject_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         testProject = TestProject.objects.get(pk=pk)
#     except TestProject.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = TestProjectSerializer(testProject)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = TestProjectSerializer(testProject, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         testProject.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# from rest_framework.views import APIView
# class TestProjectList(APIView):
#     #APIView实际继承django总的View
#     #from django.views.generic import View
#     """
#     描述TestProject List的接口
#     """
#     def get(self,request,format=None):
#         testProject  = TestProject.objects.all()
#         serializer = TestProjectSerializer(testProject,many=True)
#         return Response(serializer.data)
#
#     def post(self,request,format=None):
#         serializer = TestProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
#
# class TestProjectDetail(APIView):
#     """
#     读取, 更新 or 删除一个代码片段(TestProject)实例(instance).
#     """
#     def get_object(self,pk):
#         try:
#             return TestProject.objects.get(pk=pk)
#         except TestProject.DoesNotExist:
#             raise status.HTTP_404_NOT_FOUND
#
#     def get(self, request, pk, format=None):
#         testProject = self.get_object(pk)
#         serilizer = TestProjectSerializer(testProject)
#         return Response(serilizer.data)
#
#     def put(self,request,pk,format=None):
#         testProject = self.get_object(pk)
#         serializer = TestProjectSerializer(testProject,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,pk,format=None):
#         testProject = self.get_object(pk)
#         testProject.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import generics
from django.contrib.auth.models import User
from polls.serializers import UserSerializer
from rest_framework import permissions
from polls.permissions import IsOwnerOrReadOnly

class TestProjectList(generics.ListCreateAPIView):
    queryset = TestProject.objects.all()
    serializer_class = TestProjectSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get(self, request, *args, **kwargs):
    #     return Response(request.session['username'])

class TestProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestProject.objects.all()
    serializer_class = TestProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#创建TestCase视图集
from django.contrib.auth import  get_user_model
from rest_framework import authentication,permissions,viewsets
from .models import TestCase
from .serializers import TestCaseSerializer

class DefaultsMixin(object):
    """Default settings for view authentication, permissions, filtering and pagination."""
    authentication_classes = (
        authentication.BaseAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

class TestCaseViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,IsAuthenticatedOrReadOnly)
    def get_object(self):
        print("hello")
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    """API endpoint for listing test cases."""
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    # def perform_create(self,serializer):
    #     print(self.request.user)
    #     serializer.save(owner=User.objects.get(id=self.request.session.get('username')))
    def get(self, request, *args, **kwargs):
        print(request.user)
        return Response("hello")
    def list(self, request, *args, **kwargs):
        print(request.session.get("username"))
        queryset = TestCase.objects.filter(test_suit__owner=request.session.get("username"))
        # queryset = TestCase.objects.all()
        serializer = TestCaseSerializer(queryset, many=True)
        return Response(serializer.data)

