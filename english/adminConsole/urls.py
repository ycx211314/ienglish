# --*-- coding:utf-8 --*--
import english.adminConsole.views as view

__author__ = 'Administrator'
from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url(r"^index.html$",view.index),
    url(r"^login/$",view.loginPre),
    url(r"^login/auth/$",view.adminLogin),
    url(r"user/$",view.userIndex),
    url(r"user/list/$",view.userlist),
    url(r"news/$",view.newIndex),
    url(r"news/list/$",view.newslist),
)

