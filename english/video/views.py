# Create your views here.
# --*-- coding:utf-8 --*--
import datetime
import os
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
#跳转到主页
from django.template import RequestContext
from english.urlConfig import urlMatch
from english.video.models import OpenCourse,CourseDetail

def openCourse(request,cid):
    try:
        id =int(cid)
    except:
        Http404()
    course = OpenCourse.objects.get(id=id)
    courseDetail = CourseDetail.objects.filter(courseId=course.id).all()
    pagedict = {
        "course":course,
        "detail":courseDetail,
        "nav":urlMatch(request.path),
    }
    return render_to_response(r'video'+os.path.sep+'openCourse.html',pagedict,context_instance=RequestContext(request))