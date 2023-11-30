from django.contrib import admin
from .models import ImageFile, UserInfo, UserNotes
# Register your models here.

@admin.register(UserInfo)
class UserInfo(admin.ModelAdmin):
    list_display = ['username', 'email']

@admin.register(UserNotes)
class UserNotes(admin.ModelAdmin):
    list_display = ['pk', 'username', 'title']

@admin.register(ImageFile)
class ImageFile(admin.ModelAdmin):
    list_display = ['pk', 'user_note', 'image']
    