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
from polls.models import TestProject,TestSuit,TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        # fields = '__all__'
        # fields = '__all__'xclude('url')
        # 创建表单的时候，url，real_result不用填
        exclude = ['url','real_Result']


    def __init__(self, *args, **kwargs):
        super(TestCaseForm, self).__init__(*args, **kwargs)
        self.fields['url_param'].required = False

    #
    # def testCaseForm(self,request):
    #     if request.method == 'POST':
    #         form = TestCaseForm(request.POST)
    #         if form.is_valid():
    #             testSuit = form.cleaned_data['test_suit']
    #             name = form.cleaned_data['name']
    #             form.save()
    #             return HttpResponse('testSuit:' + testSuit + " ;name=" + name)
    def save(self, commit=True):
        super(TestCaseForm,self).save()


class TestProjectForm(forms.ModelForm):
    class Meta:
        model = TestProject
        fields = '__all__'

class TestSuitForm(forms.ModelForm):
    class Meta:
        model = TestSuit
        fields = '__all__'
