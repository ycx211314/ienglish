# --*-- coding:utf-8 --*--
import english.article.views as view

__author__ = 'Administrator'
from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url(r"^$",view.moreRead),
    url(r"^article/detail/(\d+)/$",view.articleShow),
    url(r"^english/detail/(\d+)/$",view.businessShow),
)

