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
from polls.models import TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = '__all__'


    def testCaseForm(self,request):
        if request.method == 'POST':
            form = TestCaseForm(request.POST)
            if form.is_valid():
                testSuit = form.cleaned_data['test_suit']
                name = form.cleaned_data['name']
                form.save()
                return HttpResponse('testSuit:' + testSuit + " ;name=" + name)
