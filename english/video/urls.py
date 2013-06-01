# --*-- coding:utf-8 --*--
import english.video.views as view

__author__ = 'Administrator'
from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url(r'^open/detail/(\d+)/$',view.openCourse),
)

