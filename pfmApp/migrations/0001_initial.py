# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-05-03 02:25
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JmeterSvrModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='测试计划名称')),
                ('hostIP', models.GenericIPAddressField(verbose_name='Jmeter主机IP')),
                ('agentIP', jsonfield.fields.JSONField(default='{}', help_text='暂且为空', verbose_name='执行机IP')),
                ('username', models.CharField(max_length=64, verbose_name='Jmeter主机用户名')),
                ('password', models.CharField(max_length=64, verbose_name='Jmeter主机密码')),
                ('remotePath', models.CharField(max_length=64, verbose_name='Jmeter安装路径')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='PfmCaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='用例名称')),
                ('scriptName', models.CharField(max_length=64, verbose_name='脚本名称')),
                ('step', models.IntegerField(verbose_name='单次增加的线程数')),
                ('count', models.IntegerField(verbose_name='计划执行次数')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
