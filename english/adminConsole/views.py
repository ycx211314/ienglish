# Create your views here.
# --*-- coding:utf-8 --*--
from django.http import Http404, HttpResponseRedirect
import os
from django.contrib.auth import authenticate,login,logout
from english.util.decorator.webDecorator import render

def adminLogin(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return render(r"adminConsole"+os.path.sep+"login.html",{},request)
    else:
    #验证失败，暂时不做处理
        return HttpResponseRedirect("/console/login/")

def loginPre(request):
    return render(r"adminConsole"+os.path.sep+"login.html",{},request)
    #return store_view(request)
def index(request):
    if request.session.get('adminUU'):
        return render(r"adminConsole"+os.path.sep+"index.html",{},request)
    else:
        return HttpResponseRedirect("/console/login/")

