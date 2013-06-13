# --*-- coding:utf-8 --*--
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.templatetags.static import static
import english
from english import settings
from english.commons.views import *

admin.autodiscover()

urlpatterns = patterns('',
   # url(r'^/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}, name='static'),
    #url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r"^console/",include("english.adminConsole.urls")),
    #新闻相关
    url(r"^news/",include('english.news.urls')),
    #用户相关
    url(r"^user/",include('english.studyuser.urls')),
    #资料相关
    url(r"^read/",include('english.article.urls')),
    #视频相关
    url(r"^video/",include('english.video.urls')),
    #首先相关
    url(r'^index/$',index),
    url(r'^$',index),
    url(r"^imageCode/$",imageCode),
    url(r'^task/(\w+)/$',TaskStart)
)