from django.db import models
import jsonfield

# Create your models here.


class JmeterSvrModel(models.Model):
    name = models.CharField(verbose_name="测试计划名称",max_length=64)
    hostIP = models.GenericIPAddressField(verbose_name="Jmeter主机IP")
    agentIP = jsonfield.JSONField(verbose_name="执行机IP",help_text="暂且为空",default="{}")
    username = models.CharField(verbose_name="Jmeter主机用户名",max_length=64)
    password = models.CharField(verbose_name="Jmeter主机密码",max_length=64)
    remotePath = models.CharField(verbose_name="Jmeter安装路径",max_length=64)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(JmeterSvrModel, self).save(*args, **kwargs)

class PfmCaseModel(models.Model):
    name = models.CharField(verbose_name="用例名称",max_length=64)
    scriptName = models.CharField(verbose_name="脚本名称",max_length=64)
    step = models.IntegerField(verbose_name="单次增加的线程数",)
    count = models.IntegerField(verbose_name="计划执行次数",)
    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

