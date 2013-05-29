# --*-- coding:utf-8 --*--
from django.contrib import admin
from english.news.models import News

__author__ = 'Administrator'
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','hot','readCount','createDate',)
    search_fields = ('title','titleEnglish','content','contentEnglish',)
    list_filter = ('createDate','hot',)
    date_hierarchy = 'createDate'
    ordering = ('-createDate',)
    fields = ('title','titleEnglish','content','contentEnglish','hot','imageShow','comeFrom',)
    #filter_horizontal = ('title',)
admin.site.register(News,NewsAdmin)