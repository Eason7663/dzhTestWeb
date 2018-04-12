#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Eason
@file: serializers.py
@time: 2018/04/08
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from polls.models import TestProject
import time

class TestProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = TestProject
        fields = ('name','suit_number','is_enable','owner','description')

# class TestProjectSerializer(serializers.Serializer):
#     # 每一个表都可以建一个serializer，类似Django的Form  专门用于json
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=64)
#     is_enable = serializers.BooleanField(default=True)
#     suit_number = serializers.IntegerField(default=0)
#     last_modified = serializers.DateTimeField(auto_now=True)
#     # owner
#     owner = serializers.CharField(max_length=32)
#     #描述
#     description = serializers.CharField(max_length=256)
#
#     def create(self,validated_data):
#         """
#         传入验证过的数据，并创建TestProject实例
#         :param validated_data:
#         :return:
#         """
#         return TestProject.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         传入验证过的数据，并创建TestProject实例
#         :param instance:
#         :param validated_data:
#         :return:
#         """
#         instance.name = validated_data.get('name',instance.name)
#         instance.is_enable = validated_data.get('is_enable',instance.is_enable)
#         instance.suit_number = validated_data.get('suit_number',instance.suit_number)
#         instance.last_modified = validated_data.get('last_modified',instance.suit_number)
#         instance.owner = validated_data.get('last_modified',instance.owner)
#         instance.description = validated_data.get('last_modified',instance.description)
#         instance.save()
#         return instance



class UserSerializer(serializers.ModelSerializer):
    testProjects = serializers.PrimaryKeyRelatedField(many=True, queryset=TestProject.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'testProjects')