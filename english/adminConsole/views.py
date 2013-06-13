# Create your views here.
# --*-- coding:utf-8 --*--
from django.http import Http404, HttpResponseRedirect, HttpResponse
import os
from django.contrib.auth import authenticate,login,logout
from english.adminConsole.models import *
from english.util.decorator.webDecorator import render, consoleRender

#管理员登录
from english.news.encoder import getJson
from english.studyuser.models import StudyUser
from english.news.models import News

def adminLogin(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/console/index.html")
        #return render(r"adminConsole"+os.path.sep+"index.html",{},request)
    else:
    #验证失败，暂时不做处理
        return HttpResponseRedirect("/console/login/")
#进入登录页
def loginPre(request):
    return consoleRender(r"adminConsole"+os.path.sep+"login.html",{},request)
    #return store_view(request)
#管理首页
def index(request):
    if request.user:
        return consoleRender(r"adminConsole"+os.path.sep+"index.html",{},request)
    else:
        return HttpResponseRedirect("/console/login/")

def userIndex(request):
    return consoleRender(r"adminConsole"+os.path.sep+"user"+os.path.sep+"user.html",{},request)

def userlist(request):
    page = 1
    pageSize = 10
    if request.POST.get("page") and request.POST.get("pagesize"):
        try:
            page = int(request.POST["page"])
            pageSize = int(request.POST["pagesize"])
        except:
            page = 1
            pageSize = 10
    users = StudyUser.objects.order_by("-regDate").all();
    if len(users)%pageSize !=0 and int(len(users)/pageSize) == page:
        end = pageSize*(page-1)+len(users)%pageSize
    else:
        end = pageSize*page
    json = getJson({"rows":users[(page-1)*pageSize:end],"total":len(users)})
    return HttpResponse(json)

def newIndex(request):
    return consoleRender(r"adminConsole"+os.path.sep+"news"+os.path.sep+"news.html",{},request)
def newslist(request):
    page = 1
    pageSize = 10
    if request.POST.get("page") and request.POST.get("pagesize"):
        try:
            page = int(request.POST["page"])
            pageSize = int(request.POST["pagesize"])
        except:
            page = 1
            pageSize = 10
    users = News.objects.order_by("-createDate").all();
    if len(users)%pageSize !=0 and int(len(users)/pageSize) == page:
        end = pageSize*(page-1)+len(users)%pageSize
    else:
        end = pageSize*page
    json = getJson({"rows":users[(page-1)*pageSize:end],"total":len(users)})
    return HttpResponse(json)




