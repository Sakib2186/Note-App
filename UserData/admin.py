from django.contrib import admin
from . models import UserInfo,UserNotes,Notes_Images
# Register your models here.

@admin.register(UserInfo)
class UserInfo(admin.ModelAdmin):
    list_display = ['username', 'email']

@admin.register(UserNotes)
class UserNotes(admin.ModelAdmin):
    list_display = ['pk','username','title']

@admin.register(Notes_Images)
class Notes_Images(admin.ModelAdmin):
    list_display=['note_id','image']