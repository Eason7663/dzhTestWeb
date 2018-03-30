from django.contrib import admin
from .models import TestProject,TestSuit,TestCase

# Register your models here.
admin.site.register(TestProject)
admin.site.register(TestSuit)
admin.site.register(TestCase)