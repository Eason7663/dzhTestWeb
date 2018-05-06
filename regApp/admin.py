from django.contrib import admin
from .models import TestProjectModel,TestSuitModel,TestCaseModel

# Register your models here.
admin.site.register(TestProjectModel)
admin.site.register(TestSuitModel)
admin.site.register(TestCaseModel)