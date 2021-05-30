from django.contrib import admin
from .models import QrCode, DynamicString
# Register your models here.

admin.site.register(QrCode)
admin.site.register(DynamicString)
