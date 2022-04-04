from django.contrib import admin
from app.models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # list_display用于设置列表页面要显示的不同字段
    list_display = ['id','name','tel','password']
    # search_fields用于设置搜索栏中要搜索的不同字段
    search_fields = ['id','name','tel','password']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # list_display用于设置列表页面要显示的不同字段
    list_display = ['id','user','time','jingdian','content','score']
    # search_fields用于设置搜索栏中要搜索的不同字段
#
#
# @admin.register(NewsType)
# class NewsTypeAdmin(admin.ModelAdmin):
#     # list_display用于设置列表页面要显示的不同字段
#     list_display = ['id', 'name']
#     # search_fields用于设置搜索栏中要搜索的不同字段
#     search_fields = ['id', 'name']
#
#
# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#     # list_display用于设置列表页面要显示的不同字段
#     list_display = ['id', 'title', 'date', 'img','type','content','keywords','url','source']
#     # search_fields用于设置搜索栏中要搜索的不同字段
#     search_fields = ['id', 'title', 'date', 'img','type','content','keywords','url','source']
#
