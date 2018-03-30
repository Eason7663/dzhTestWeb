# Generated by Django 2.0.3 on 2018-03-29 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
    ]
