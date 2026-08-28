from django.contrib import admin
from .models import Category, Ad

# تسجيل جدول الأقسام وجدول الإعلانات في لوحة التحكم
admin.site.register(Category)
admin.site.register(Ad)