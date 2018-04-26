#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     forms
   Description :
   Author :       Eason
   date：          2018/4/17
-------------------------------------------------
   Change Activity:
                   2018/4/17:
-------------------------------------------------
"""
from django import forms
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from pfmApp.models import JmeterSvrModel

class JmeterSvrModelForm(forms.ModelForm):
    class Meta:
        model = JmeterSvrModel
        fields = '__all__'
