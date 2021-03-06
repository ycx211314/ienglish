# --*-- coding:utf-8 --*--
import english.news.views as view

__author__ = 'Administrator'
from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url(r'^(\d+)/$',view.newsMore),
    url(r'^$',view.newsMore),
    url(r"^type/(\w+)/$",view.newsTypeMore),
    url(r"^type/(\w+)/(\d+)/$",view.newsTypeMore),
    url(r'^detail/(\d+)/$',view.newDetail),
    url(r"^read/(\d+)/$",view.readNews),
    url(r'^comment/add/$',view.addCommont),
    url(r"comment/(\d+)/$",view.showComment),
    url(r"comment/(\d+)/(\d+)/$",view.showComment),
    url(r"comment/agree/up/$",view.agreeWith),
)

