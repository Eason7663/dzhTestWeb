from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


from polls.models import TestProject, TestSuit,TestCase
from polls.serializers import TestProjectSerializer
import time


# 首页(登录)
def index(request):
    # tp = TestProject()
    # tp.save()
    # return HttpResponse('id = {}'.format(tp.name))

    # return render(request,'index.html')

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
            response = HttpResponseRedirect('/testproject_manage/') # 登录成功跳转发布会管理
            request.session['username'] = username    # 将 session 信息写到服务器
            return response
            # return HttpResponse('HELLO')
        else:
            return render(request,"polls/index.html",{"error":"username or password error!"})
    # 防止直接通过浏览器访问 /login_action/ 地址。
    return render(request,"index.html")

#test project管理页面
@login_required
def testproject_manage(request):
    testprojects_list = TestProject.objects.all()
    username = request.session.get('username', '')
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
def help_document(request,args):
    # detect if args is well-format

    try:
        article_id = int(args)
    except:
        return HttpResponse("Invalid Article Number...")

    article_list = Article.objects.all()
    if article_id not in range(1, len(article_list) + 1):
        return HttpResponse("Invalid Article Number...")

    atc = Article.objects.get(id=article_id)
    template = loader.get_template('show_atc.html')

    # show markdown text
    mfile = open('./../../django-markdown-deux.md', 'r').read()
    atc.content = mfile

    return_dict = {'title': atc.title, 'category': atc.category, 'date': atc.date_time, 'content': atc.content}
    return HttpResponse(template.render(return_dict, request))

# 执行用例
def execute_case_action(request,case_id):
    time.sleep(1)
    if(case_id == "1"):
        return HttpResponse("failed")
    if(case_id == "2"):
        return HttpResponse("pass")

#返回json格式test project
@api_view(['GET','POST'])
def testProject_list(request):
    """
    List all testproject, or create a new testproject.
    :param request:
    :return:
    """
    if request.method == 'GET':
        testProject = TestProject.objects.all()
        serializer = TestProjectSerializer(testProject,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TestProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # serializer.data 数据创建成功后所有数据
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # serializer.errors 错误信息
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def testProject_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        testProject = TestProject.objects.get(pk=pk)
    except TestProject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TestProjectSerializer(testProject)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TestProjectSerializer(testProject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        testProject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)