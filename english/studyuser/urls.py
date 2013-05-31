# --*-- coding:utf-8 --*--
import english.studyuser.views as view

__author__ = 'Administrator'
from django.conf.urls.defaults import patterns,url
urlpatterns = patterns('',
    url(r'^registerpre/$',view.regPre),
    url(r'^register/$',view.reg),
    url(r'^check/$',view.userExsit),
    url(r'^login/$',view.login),
    url(r'^logout/$',view.logout),
)

