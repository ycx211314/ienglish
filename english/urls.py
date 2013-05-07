from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.templatetags.static import static
from english import settings
from english.common.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT},name="static"),
    # url(r'^$', 'english.views.home', name='home'),
    # url(r'^english/', include('english.foo.urls')),
    url(r'^/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT},name="upload"),
    #url(r'^/static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ADMIN_MEDIA_PREFIX}, name='staticfile'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/$',newsMore),
    url(r'^news/detail/(\d+)/$',newDetail),
    url(r'^index/$',index),
    url(r'^user/login/$',login),
    url(r'^user/logout/$',logout),
    url(r'^$',index),
    url(r'^task/(\w+)/$',TaskStart)
)
