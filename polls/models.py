from __future__ import unicode_literals
from django.db import models

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
import jsonfield

# Create your models here.
class TestProject(models.Model):
    #主键 project_id
    #id 主键， by default, django gives each model the field named id (id = models.AutoField(primary_key=True))
    # 名称
    name = models.CharField(max_length=64)
    is_enable = models.BooleanField(default=True)
    suit_number = models.BigIntegerField(default=0,null=True)
    last_modified = models.DateTimeField(auto_now=True,null=True)
    # owner
    owner = models.CharField(max_length=64)
    #描述
    description = models.CharField(max_length=256)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        # lexer = get_lexer_by_name(self.language)
        # linenos = self.linenos and 'table' or False
        # options = self.title and {'title': self.title} or {}
        # formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        # self.highlighted = highlight(self.code, lexer, formatter)
        super(TestProject, self).save(*args, **kwargs)

class TestSuit(models.Model):
    test_project = models.ForeignKey(TestProject, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=64)
    is_enable = models.BooleanField(default=True)
    case_number = models.BigIntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.CharField(max_length=64)
    pass_case = models.IntegerField()
    fail_case = models.IntegerField()
    #描述
    description = models.CharField(max_length=256)
    on_going = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

class TestCase(models.Model):
    test_suit = models.ForeignKey(TestSuit,on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=64,verbose_name="名称")
    is_enable = models.BooleanField(default=True,verbose_name="状态")
    url_path = models.CharField(max_length=64,verbose_name="Path",help_text="样例：/a/b 以‘/’开头")
    # url_param = models.TextField()
    url_param = jsonfield.JSONField(verbose_name="Param",null=True,help_text="Tip：确认Josn格式有效，或者为空")
    # real_Result = models.TextField()
    real_Result = jsonfield.JSONField(verbose_name="实际结果",null=True,help_text="Tip：确认Josn格式有效，或者为空")
    # expected_result = models.TextField()
    expected_result = jsonfield.JSONField(verbose_name="期望结果",null=True,help_text="Tip：确认Josn格式有效，必选")
    pass_or_fail = models.BooleanField(default=None,verbose_name="执行结果")
    description = models.CharField(max_length=256,verbose_name="描述",null=True)
    on_going = models.BooleanField(default=True,verbose_name="正在执行")
    url = models.URLField(default="http://127.0.0.1:8001/",verbose_name="完整URL",null=True)
    owner = models.CharField(default='',max_length=32,null=True)

    def __str__(self):
        return self.name
