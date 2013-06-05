# Create your views here.
from django.http import Http404
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from english.article.models import *
from english.urlConfig import urlMatch
from english.util.decorator.webDecorator import loadNav, render

def moreRead(request):
    return render(r"resource"+os.path.sep+"moreRead.html",{},request)
def articleShow(request,artId):
    try:
        id = int(artId)
    except ValueError:
        raise Http404()
    shortArt = ShortArticel.objects.filter(id=id)[0]
    return render(r'resource'+os.path.sep+'artcicle.html', {"artcicle": shortArt}, request)
def businessShow(request,bid):
    try:
        id = int(bid)
    except ValueError:
        raise Http404()
    shortArt = BusinessEssay.objects.filter(id=id)[0]
    return render(r'resource'+os.path.sep+'business.html', {"artcicle": shortArt},request)
