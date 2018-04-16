from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# Create your models here.
class TestProject(models.Model):
    #主键 project_id
    #id 主键， by default, django gives each model the field named id (id = models.AutoField(primary_key=True))
    # 名称
    name = models.CharField(max_length=64)
    is_enable = models.BooleanField(default=True)
    suit_number = models.BigIntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
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
    owner = models.CharField(max_length=32)
    pass_case = models.IntegerField()
    fail_case = models.IntegerField()
    #描述
    description = models.CharField(max_length=256)
    on_going = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

class TestCase(models.Model):
    test_suit = models.ForeignKey(TestSuit,on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=64)
    is_enable = models.BooleanField(default=True)
    url_path = models.CharField(max_length=64)
    url_param = models.TextField()
    real_Result = models.TextField()
    expected_result = models.TextField()
    pass_or_fail = models.BooleanField(default=None)
    description = models.CharField(max_length=256)
    on_going = models.BooleanField(default=True)
    url = models.URLField(default=None)

    def __str__(self):
        return self.name
