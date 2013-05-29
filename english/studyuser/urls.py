# --*-- coding:utf-8 --*--
import english.studyuser.views as view

__author__ = 'Administrator'
from django.conf.urls.defaults import patterns,url
urlpatterns = patterns('',
    url(r'^registerpre/$',view.RegPre),
    url(r'^register/$',view.Reg),
    url(r'^check/$',view.userExsit),
    url(r'^login/$',view.login),
    url(r'^logout/$',view.logout),
)

