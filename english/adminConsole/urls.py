# --*-- coding:utf-8 --*--
import english.adminConsole.views as view

__author__ = 'Administrator'
from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url(r"^$",view.index),
    url(r"^login/$",view.loginPre),
    url(r"^login/auth/$",view.adminLogin),
)

