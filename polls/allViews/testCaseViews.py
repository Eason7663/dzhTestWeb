#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: testCaseViews.py
@time: 2018/04/15
"""

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

#test case管理页面
@login_required
def testcase_manage(request):
    testcases_list = TestCase.objects.all()
    username = request.session.get('username', '')
    return render(request, "polls/testcase_manage.html", {"user": username,"testcases":testcases_list})