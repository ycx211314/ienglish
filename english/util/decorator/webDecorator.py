# --*-- coding:utf-8 --*--
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from english.adminConsole.models import Menu
from english.urlConfig import urlMatch

__author__ = 'Administrator'

def loadNav(fn):
    def request(*args, **kwds):
        args[1]["nav"] = urlMatch(args[2].path)
        fs = fn(*args,**kwds)
        return fs
    return request
@loadNav
def render(template,args,request):
    return render_to_response(template,args,context_instance=RequestContext(request))
def consoleRender(template,args,request):
    args["nav"] = request.path
    args['menus'] = Menu.objects.filter(show=True,level = 0).all()
    return render_to_response(template,args,context_instance=RequestContext(request))