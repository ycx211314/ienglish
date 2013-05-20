# Create your views here.
# --*-- coding:utf-8 --*--
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response

#跳转到主页
from django.template import RequestContext
from english.article.models import ShortArticel
from english.common.encoder import getJson
from english.common.models import News, StudyUser

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
    newsall = News.objects.all()[0:10]
    nav = urlMatch(request.path)
    return render_to_response(r'news\news_more.html', {"newses":newsall,"nav":nav}, context_instance=RequestContext(request))


def newDetail(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    news = News.objects.filter(id=offset)[0]
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
    nav = urlMatch(request.path)
    return render_to_response(r'news\newsdetail.html', {"news": news,"content":contentDict,"nav":nav}, context_instance=RequestContext(request))


def TaskStart(request,comand):
    if comand and str(comand) == "start":
        task = NewsTask()
        task.start()
    if comand and str(comand) == "art":
        task = ArticleTask()
        task.start()
    return HttpResponse("/admin/login/")
#注册前信息查询
def RegPre(request):
    print(r'查询注册使用的信息，地市 and so on')
    return render_to_response(r'regist.html')

def Reg(request):
    print ('注册操作')
    return render_to_response(r'forward.html',{'alertMessage':'注册成功','redirectUrl':'/index'});