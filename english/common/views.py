# Create your views here.
# --*-- coding:utf-8 --*--
import datetime
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response

#跳转到主页
from django.template import RequestContext
from english.article.models import ShortArticel
from english.common.encoder import getJson
from english.common.models import News, StudyUser, Comment

#进入首页
from english.urlConfig import urlMatch
from english.util.Task import NewsTask, ArticleTask

def index(request):
    news = News.objects.order_by("-createDate").all()[:10] #查询新闻前5条
    shortArticle = ShortArticel.objects.order_by("-pointCount").all()[:10]
    nav = urlMatch(request.path)
    return render_to_response('index.html', {"news": news,"nav":nav,"article":shortArticle}, context_instance=RequestContext(request))
#用户登录
def login(request):
    if request.method == 'POST':
        if 'username' in request.POST and request.POST['username'] and 'password' in request.POST and request.POST[
                                                                                                      'password']:
            name = request.POST['username']
            psw = request.POST['password']
            student = StudyUser.objects.filter(userName=name, passwords=psw)
            if len(student):
                stu = student[0]
                stu.passwords='null'
                request.session['loginFlag'] = True
                request.session['login'] = stu
                json = getJson({'login':stu,'flag':'ok'})
        else:
            json = getJson({'flag':'no'})
        return HttpResponse(json)
#用户退出
def logout(request):
    if request.method == 'GET':
        try:
            del request.session['loginFlag']
            del request.session['login']
            json = getJson({'flag':'ok'})
        except KeyError:
            pass
        return HttpResponse(json)
#新闻相关
def newsMore(request,page=1):
    try:
        page = int(page)
    except ValueError:
        raise Http404()
    st = (page -1) * 10
    ed = page * 10
    newsall = News.objects.all()
    topNews = News.objects.order_by("-readCount").all()[0:10]
    topShare = newsall.order_by("-shareCount")[0:10]
    total = len(newsall)
    if total % 10 == 0:
        pages = total / 10
    else:
        pages = int((total + 10) / 10)
    panations = []
    if page > 1:
        panations.append(page-1)
    else:
        panations.append(1)
    if page < 5:
        for x in range(1,11):
            panations.append(x)
            if x >=  pages:
                break
    else:
        for x in range(page - 1,page - 1 + 10):
            panations.append(x)
            if x > pages:
                break
    if page+1 > pages:
        panations.append(page)
    else:
        panations.append(page+1)
    nav = urlMatch(request.path)
    pagedict = {"newses":newsall[st:ed],
                "topNews": topNews,
                "topShare":topShare,
                "nav":nav,
                "panation":panations,
                "lastPage":pages,
                "curPage":page}
    return render_to_response(r'news/news_more.html',pagedict,context_instance=RequestContext(request))
def newDetail(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    news = News.objects.get(id=offset)
    contentEN = news.content.split("###")
    contetnCH = news.contentEnglish.split("###")
    contentDict = []
    index = 0
    while index < len(contentEN):
        if len(contentEN[index]) == 0:
            index = index +1
            continue
        else:
            contentDict.append('<p class="english">'+contentEN[index]+'</p>')
            contentDict.append('<p class="englishCH" id="tip'+str(index)+'">'+contetnCH[index]+'</p>')
        index = index +1
    comments = Comment.objects.filter(news = offset).order_by("-createTs").all()
    nav = urlMatch(request.path)
    return render_to_response(r'news/newsdetail.html', {"news": news,"content":contentDict,"nav":nav,"comments":comments}, context_instance=RequestContext(request))
def readNews(request,id):
    try:
        id = int(id)
    except ValueError:
        pass
    updateVo = News.objects.get(id=id)
    count = updateVo.readCount + 1
    News.objects.filter(id=id).update(readCount = count)
    json = getJson({'flag':'ok'})
    return HttpResponse(json)

def addCommont(request):
    if request.method == 'POST':
        newId = request.POST['newsId']
        comment = Comment()
        comment.message =  request.POST['comment']
        comment.user = request.session['login']
        comment.news = News.objects.get(id=newId)
        comment.createTs = datetime.datetime.now()
        comment.save()
        json = getJson({'flag':'ok'})
    else:
        json = getJson({'flag':'no'})
    return HttpResponse(json)
def TaskStart(request,comand):
    if comand and str(comand) == "start":
        task = NewsTask()
        task.start()
    if comand and str(comand) == "art":
        task = ArticleTask()
        task.start()
    return HttpResponse("/admin/login/")
