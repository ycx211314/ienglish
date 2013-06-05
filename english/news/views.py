# --*-- coding:utf-8 --*--
import datetime,os
from django.http import Http404, HttpResponse

#跳转到主页
from django.template import RequestContext
from english.news.encoder import getJson
from english.news.models import News, Comment, NewsCategory

#进入首页
from english.urlConfig import urlMatch
#新闻相关
from english.util.decorator.webDecorator import render

def newsMore(request,page=1):
    try:
        page = int(page)
    except ValueError:
        raise Http404()
    st = (page -1) * 10
    ed = page * 10
    newsall = News.objects.order_by("-createDate").all()
    category = NewsCategory.objects.order_by("typeOrder").all();
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
                'category':category,
                "panation":panations,
                "lastPage":pages,
                "curPage":page}
    return render(r'news'+os.path.sep+'news_more.html',pagedict,request)
def newsTypeMore(request,type,page=1):
    try:
        page = int(page)
        typeStr = str(type)
    except ValueError:
        raise Http404()
    except Exception:
        raise Http404()
    st = (page -1) * 10
    ed = page * 10
    curCate = NewsCategory.objects.get(typeUrl=typeStr)
    category = NewsCategory.objects.order_by("typeOrder").all();
    if not curCate:
        raise Http404()
    else:
        newsall = curCate.news_set.order_by("-createDate").all()
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
                "curCate":curCate,
                'category':category,
                "panation":panations,
                "lastPage":pages,
                "curPage":page}
    return render(r'news'+os.path.sep+'news_type_more.html',pagedict,request)
def newDetail(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    news = News.objects.get(id=offset)
    contentEN = news.contentEnglish.split("|||")
    contetnCH = news.content.split("|||")
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
    return render(r'news'+os.path.sep+'newsdetail.html', {"news": news,"content":contentDict,"comments":comments,"newsRes":news.newsres_set.all()}, request)
def readNews(request,id):
    try:
        id = int(id)
    except ValueError:
        pass
    if request.GET["share"]:
        try:
            share = int(request.GET["share"])
        except:
            share = 0
    updateVo = News.objects.get(id=id)
    count = updateVo.readCount + 1
    commentCount = len(updateVo.comment_set.all())
    if share != 0:
        News.objects.filter(id=id).update(readCount = count,shareCount=share,commentCount = commentCount )
    else:
        News.objects.filter(id=id).update(readCount = count,commentCount = commentCount )
    json = getJson({'flag':'ok'})
    return HttpResponse(json)

def addCommont(request):
    if request.method == 'POST':
        newId = request.POST['newsId']
        comment = Comment()
        comment.message =  request.POST['comment']
        comment.user = request.session['login']
        comment.ipAddr = request.POST['ip']
        comment.ipName = request.POST['ipname']
        comment.news = News.objects.get(id=newId)
        comment.createTs = datetime.datetime.now()
        comment.save()
        json = getJson({'flag':'ok'})
    else:
        json = getJson({'flag':'no'})
    return HttpResponse(json)
def showComment(request,newsId,page=1):
    pageSize = 5
    try:
        id = int(newsId)
        page = int(page)
    except:
        return Http404()
    news = News.objects.get(id=id)
    commonts =news.comment_set.order_by("-createTs").all()
    total = len(commonts)
    st = (page -1) * pageSize
    ed = page * pageSize
    if total % pageSize == 0:
        pages = total / pageSize
    else:
        pages = int((total + pageSize) / pageSize)
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
    return  render(r'news'+os.path.sep+'comment.html',{"comments":commonts[st:ed],
                                                                   'news':news,
                                                                   "curPage":page,
                                                                   "lastPage":pages,
                                                                   "panation":panations},request)
def agreeWith(request):
    """
    评论赞同
    """
    res = {"flag":"no"}
    if request.GET["comId"]:
        try:
            commentId = int(request.GET["comId"])
        except:
            res["flag"]="no"
    comment = Comment.objects.get(id=commentId)
    comment.agreeWith = comment.agreeWith + 1
    comment.save()
    res["flag"]="ok"
    return HttpResponse(getJson(res))