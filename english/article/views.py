# Create your views here.
from django.http import Http404
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from english.article.models import *
from english.urlConfig import urlMatch

def articleShow(request,artId):
    try:
        id = int(artId)
    except ValueError:
        raise Http404()
    shortArt = ShortArticel.objects.filter(id=id)[0]
    nav = urlMatch(request.path)
    return render_to_response(r'resource'+os.path.sep+'artcicle.html', {"artcicle": shortArt,"nav":nav,}, context_instance=RequestContext(request))
def businessShow(request,bid):
    try:
        id = int(bid)
    except ValueError:
        raise Http404()
    shortArt = BusinessEssay.objects.filter(id=id)[0]
    nav = urlMatch(request.path)
    return render_to_response(r'resource'+os.path.sep+'business.html', {"artcicle": shortArt,"nav":nav,}, context_instance=RequestContext(request))
