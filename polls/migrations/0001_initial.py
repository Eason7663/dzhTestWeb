# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-04-30 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('is_enable', models.BooleanField(default=True, verbose_name='状态')),
                ('url_path', models.CharField(help_text='样例：/a/b 以‘/’开头', max_length=64, verbose_name='Path')),
                ('url_param', jsonfield.fields.JSONField(help_text='Tip：确认Josn格式有效，或者为空', null=True, verbose_name='Param')),
                ('real_Result', jsonfield.fields.JSONField(help_text='Tip：确认Josn格式有效，或者为空', null=True, verbose_name='实际结果')),
                ('expected_result', jsonfield.fields.JSONField(help_text='Tip：确认Josn格式有效，必选', null=True, verbose_name='期望结果')),
                ('pass_or_fail', models.BooleanField(default=None, verbose_name='执行结果')),
                ('description', models.CharField(max_length=256, null=True, verbose_name='描述')),
                ('on_going', models.BooleanField(default=True, verbose_name='正在执行')),
                ('url', models.URLField(default='http://127.0.0.1:8001/', null=True, verbose_name='完整URL')),
                ('owner', models.CharField(default='', max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_enable', models.BooleanField(default=True)),
                ('suit_number', models.BigIntegerField(default=0, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('owner', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='TestSuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_enable', models.BooleanField(default=True)),
                ('case_number', models.BigIntegerField(default=0)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('owner', models.CharField(max_length=64)),
                ('pass_case', models.IntegerField()),
                ('fail_case', models.IntegerField()),
                ('description', models.CharField(max_length=256)),
                ('on_going', models.BigIntegerField(default=0)),
                ('test_project', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='polls.TestProject')),
            ],
        ),
        migrations.AddField(
            model_name='testcase',
            name='test_suit',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='polls.TestSuit'),
        ),
    ]
