# Create your views here.
# --*-- coding:utf-8 --*--
import datetime
from django.http import Http404, HttpResponse

#跳转到主页
from django.template import RequestContext
from english.article.models import *
from english.news.models import News
from english.util.decorator.webDecorator import render
from english.video.models import *

#进入首页
from english.urlConfig import urlMatch
from english.util.Task import NewsTask, ArticleTask, BusinessTask,CourseTask

def index(request):
    news = News.objects.order_by("-createDate").all()[:10] #查询新闻前5条
    carouselNews = News.objects.order_by("-readCount").filter(contentType=2).all()[0:5] #滚动
    hotNews = News.objects.filter(hot=True).all()[0:10]
    shortArticle = ShortArticel.objects.order_by("-pointCount").all()[:10]   #精美短文
    businessArt = BusinessEssay.objects.order_by("-createDate").all()[:10]
    course = OpenCourse.objects.all()[0:10] #相关课程
    nav = urlMatch(request.path)
    return render('index.html', {
                                "news": news,
                                "carNews":carouselNews,
                                'hotNews':hotNews,
                                "article":shortArticle,
                                "course":course,
                                "business":businessArt}, request)
def TaskStart(request,comand):
    if comand and str(comand) == "start":
        task = NewsTask()
        task.start()
    if comand and str(comand) == "art":
        task = ArticleTask()
        task.start()
    if comand and str(comand) == 'bus':
        task = BusinessTask()
        task.start()
    if comand and  str(comand)=='course':
        task = CourseTask()
        task.start()
    return HttpResponse("starting........")
