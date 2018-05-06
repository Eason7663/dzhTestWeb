#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: TokenBackend.py
@time: 2018/05/06
"""

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator


class TokenBackend(ModelBackend):
    def authenticate(self, pk, token=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        if default_token_generator.check_token(user, token):
            return user
        return None