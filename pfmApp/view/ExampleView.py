#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: ExampleView.py
@time: 2018/05/05
"""
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse,JsonResponse

from django.contrib.auth.decorators import login_required

class ExampleView(APIView):
    # authentication scheme 局部的
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
