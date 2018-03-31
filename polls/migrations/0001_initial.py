# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-03-30 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_enable', models.BooleanField(default=True)),
                ('url_path', models.CharField(max_length=64)),
                ('url_param', models.TextField()),
                ('real_Result', models.TextField()),
                ('expected_result', models.TextField()),
                ('pass_or_fail', models.BooleanField(default=None)),
                ('description', models.CharField(max_length=256)),
                ('on_going', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_enable', models.BooleanField(default=True)),
                ('suit_number', models.BigIntegerField(default=0)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('owner', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='TestSuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_enable', models.BooleanField(default=True)),
                ('case_number', models.BigIntegerField(default=0)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('owner', models.CharField(max_length=32)),
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
