# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User

# Register your models here.

# 自己添加内容
class UserAdmin(admin.ModelAdmin):
    list_display = ('account','password','nicheng','email','haha','haha2')

admin.site.register(User,UserAdmin)