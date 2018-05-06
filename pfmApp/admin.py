from django.contrib import admin
from .models import PfmCaseModel

# Register your models here.
admin.site.register(PfmCaseModel)

from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ('user',)