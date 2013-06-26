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
    url(r"news/edit/(\d+)/$",view.newsEdit),
    url(r"news/update/$",view.newsUpdate),
    url(r"news/del/$",view.newsDel),
    url(r"news/hot/$",view.newsPointHot),
    url(r"news/pic/(\d+)/$",view.newsPic),
    url(r"news/pic/upload/$",view.newsPicUpload),
    url(r"news/pic/del/$",view.newPicDel),

    url(r"task/$",view.taskIndex),
    url(r"task/preAdd/$",view.taskAddPre),
    url(r"task/add/$",view.taskAdd),
    url(r"task/del/$",view.delTask),
    url(r"task/editPre/(\d+)/$",view.taskEditPre),
    url(r"task/edit/$",view.taskEdit),
    url(r"task/process/$",view.taskUpdate),
    url(r"task/list/$",view.taskList),
)

