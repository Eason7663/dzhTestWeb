#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: UserViews.py
@time: 2018/05/05
"""
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics
from django.contrib.auth.models import User
from regApp.serializers import UserSerializer

# 首页(登录)
def index(request):
    return render(request, "regApp/../../templates/index.html")


# 登录动作
@csrf_protect
def login_action(request):
    if request.method == "POST":
        # 寻找名为 "username"和"password"的POST参数，而且如果参数没有提交，返回一个空的字符串。
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        if username == '' or password == '':
            return render(request, "regApp/../../templates/index.html", {"error": "username or password null!"})

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user) # 验证登录
            response = HttpResponseRedirect('/regApp/testproject/home') # 登录成功跳转home页面
            request.session['username'] = username    # 将 session 信息写到服务器
            return response
            # return HttpResponse('HELLO')
        else:
            return render(request, "regApp/../../templates/index.html", {"error": "username or password error!"})
    # 防止直接通过浏览器访问 /login_action/ 地址。
    return render(request, "regApp/../../templates/index.html")

@login_required
def logout_action(request):
    auth.logout(request)
    return render(request, "regApp/../../templates/index.html")

# help文档
@login_required
def help_document(request):
    return HttpResponse("Preparing!")

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator

def token_new(request, localusername):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            user = authenticate(username = localusername, password = '')
            if user:
                data = {
                    'success': True,
                    'token': default_token_generator.make_token(user),
                    'user': user.pk,
                }
                return data
            else:
                return HttpResponse("Error token!")
    elif request.method == 'GET':
        if 'username' in request.GET and 'password' in request.GET:
            user = authenticate(username = localusername, password = '')
            if user:
                data = {
                    'success': True,
                    'token': default_token_generator.make_token(user),
                    'user': user.pk,
                }
                return data
            else:
                return HttpResponse("Error token!")
