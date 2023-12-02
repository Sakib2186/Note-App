from django.contrib import admin
from . models import UserInfo,UserNotes,NoteImage,Notes_Label
# Register your models here.

@admin.register(UserInfo)
class UserInfo(admin.ModelAdmin):
    list_display = ['username', 'email']

@admin.register(UserNotes)
class UserNotes(admin.ModelAdmin):
    list_display = ['pk','username','title','note_label','date']

@admin.register(NoteImage)
class NoteImage(admin.ModelAdmin):
    list_display=['note','image']

@admin.register(Notes_Label)
class Notes_Label(admin.ModelAdmin):
    list_display=['labelName','label_for']