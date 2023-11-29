from django.contrib import admin
from .models import UserInfo, UserNotes
# Register your models here.

@admin.register(UserInfo)
class UserInfo(admin.ModelAdmin):
    list_display = ['username', 'email']

@admin.register(UserNotes)
class UserNotes(admin.ModelAdmin):
    list_display = ['pk', 'username', 'title']
    