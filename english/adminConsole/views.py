# Create your views here.
# --*-- coding:utf-8 --*--
import uuid,os,datetime
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login
from english.adminConsole.models import ContentTask
from english.util.decorator.webDecorator import render, consoleRender
#管理员登录
from english.news.encoder import getJson
from english.studyuser.models import StudyUser
from english.news.models import News,NewsCategory, NewsRes

def adminLogin(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/console/index.html")
    else:
        return HttpResponseRedirect("/console/login/")
#进入登录页
def loginPre(request):
    return consoleRender(r"adminConsole"+os.path.sep+"login.html",{},request)
#管理首页
def index(request):
    if request.user:
        return consoleRender(r"adminConsole"+os.path.sep+"index.html",{},request)
    else:
        return HttpResponseRedirect("/console/login/")
#用户管理
def userIndex(request):
    return consoleRender(r"adminConsole"+os.path.sep+"user"+os.path.sep+"user.html",{},request)
#用户列表
def userlist(request):
    page,pageSize = 1,10
    if request.POST.get("page") and request.POST.get("rows"):
        try:
            page,pageSize = int(request.POST["page"]),int(request.POST["rows"])
        except BaseException:
            page,pageSize = 1,10
    users = StudyUser.objects.order_by("-regDate").all()
    end = pageSize*page
    if end > len(users):
        end = len(users)
    json = getJson({"rows":users[(page-1)*pageSize:end],"total":len(users)})
    return HttpResponse(json)
#双语新闻
def newIndex(request):
    category = NewsCategory.objects.order_by("-typeOrder").all()
    return consoleRender(r"adminConsole"+os.path.sep+"news"+os.path.sep+"news.html",{"category":category},request)
#双语信息列表
def newslist(request):
    page,pageSize =1,10
    if request.POST.get("page") and request.POST.get("rows"):
        try:
            page,pageSize = int(request.POST["page"]),int(request.POST["rows"])
        except BaseException:
            page,pageSize =1,10
    qList =[]
    for key in request.POST.keys():
        if key == 'categroy':
            qList.append(Q(categroy = request.POST[key]))
        if key == "contentType":
            qList.append(Q(contentType = request.POST[key]))
        if key == "hot":
            if request.POST[key] == "true":
                qList.append(Q(hot = True))
            else:
                qList.append(Q(hot = False))
        if key == 'titleLike':
            qList.append(Q(title__contains=request.POST[key]))
    start,end = datetime.datetime.strptime("2009-01-01",'%Y-%m-%d'),datetime.datetime.now()
    if "startTs" in request.POST.keys():
        start = datetime.datetime.strptime(request.POST["startTs"],'%Y-%m-%d')
    if "endTs" in request.POST.keys():
        end = datetime.datetime.strptime(request.POST["endTs"],'%Y-%m-%d')
    qList.append(Q(createDate__range=(start,end)))
    manager = News.objects.filter()
    for q in qList:
        manager = manager.filter(q)
    if request.POST.get("order") and request.POST.get("sort"):
        order,field = request.POST["order"],request.POST["sort"]
        if order != "desc":
            field = "-"+field
        users = manager.order_by(field).all()
    else:
        users = manager.order_by("-createDate").all()
    end = pageSize*page
    if end > len(users):
        end = len(users)
    json = getJson({"rows":users[(page-1)*pageSize:end],"total":len(users)})
    return HttpResponse(json)
#新闻编辑
def newsEdit(request,id):
    try:
        news = News.objects.get(id=int(id))
        cate = NewsCategory.objects.order_by("typeOrder").all()
    except BaseException:
        return Http404()
    return consoleRender(r"adminConsole"+os.path.sep+"news"+os.path.sep+"newsEdit.html",{"news":news,"category":cate},request)
#新闻修改
def newsUpdate(request):
    if request.POST.get("id"):
        try:
            updateNews = News.objects.get(id=int(request.POST["id"]))
            updateNews.introduce,updateNews.content,updateNews.contentEnglish = request.POST['introduce'],request.POST["content"], request.POST["contentEnglish"]
            updateNews.save()
        except BaseException as e:
            json = getJson({"flag":"no"})
        json = getJson({"flag":"yes"})
    else:
        json = getJson({"flag":"no"})
    return HttpResponse(json)
#删除新闻
def newsDel(request):
    try:
        if request.POST.get("id"):
            delNews = News.objects.get(id=int(request.POST["id"]))
            delNews.delete()
        elif request.POST.get("ids"):
            idArray = str(request.POST["ids"]).split(",")
            News.objects.filter(id__in=idArray).delete()
        else:
            json = getJson({"flag":"no"})
        json = getJson({"flag":"yes"})
    except BaseException:
        json = getJson({"flag":"no"})
    return HttpResponse(json)
#标注热点新闻
def newsPointHot(request):
    if request.POST.get("ids") and request.POST.get("hot"):
        try:
            idArray = str(request.POST["ids"]).split(",")
            if int(request.POST['hot'])==0:
                News.objects.filter(id__in=idArray).update(hot=False)
            else:
                News.objects.filter(id__in=idArray).update(hot=True)
        except BaseException:
            json = getJson({"flag":"no"})
        json = getJson({"flag":"yes"})
    else:
        json = getJson({"flag":"no"})
    return HttpResponse(json)
#新闻图片
def newsPic(request,id):
    try:
        news = News.objects.get(id=int(id))
    except BaseException:
        return Http404()
    return consoleRender(r"adminConsole"+os.path.sep+"news"+os.path.sep+"news_pic.html",{"news":news},request)
#上传图片
def newsPicUpload(request):
    if request.POST.get("id"):
        try:
            res = NewsRes()
            res.newsId = News.objects.get(id=int(request.POST["id"]))
            res.resUrl.save("IMG_"+str(id)+str(uuid.uuid1())+".jpg",request.FILES["pic"])
            res.save()
        except BaseException as e:
            json = getJson({"flag":"no"})
        json = getJson({"flag":"yes"})
    else:
        json = getJson({"flag":"no"})
    return HttpResponse(json)
#删除图片
def newPicDel(request):
    if request.POST.get("delId"):
        try:
            NewsRes.objects.get(id=int(request.POST["delId"])).delete()
        except BaseException as e:
            json = getJson({"flag":"no"})
        json = getJson({"flag":"yes"})
    else:
        json = getJson({"flag":"no"})
    return HttpResponse(json)
#任务页面
def taskIndex(request):
    return  consoleRender(r"adminConsole"+os.path.sep+"task"+os.path.sep+"task.html",{},request)
def taskList(request):
    page,pageSize =1,10
    if request.POST.get("page") and request.POST.get("rows"):
        try:
            page,pageSize = int(request.POST["page"]),int(request.POST["rows"])
        except BaseException:
            page,pageSize =1,10
    manager = ContentTask.objects.all()
    end = pageSize*page
    if end > len(manager):
        end = len(manager)
    json = getJson({"rows":manager[(page-1)*pageSize:end],"total":len(manager)})
    return HttpResponse(json)
def taskAddPre(request):
    return  consoleRender(r"adminConsole"+os.path.sep+"task"+os.path.sep+"taskAdd.html",{},request)
def taskAdd(request):
    try:
        json = getJson({"flag":"yes"})
        if request.POST.get("taskName") and request.POST.get("taskType") and request.FILES["taskFile"]:
            task = ContentTask()
            task.taskName,task.taskType,task.processFlag = request.POST["taskName"],request.POST["taskType"],"Prepare",
            task.fileName.save("TXT_"+str(uuid.uuid1())+".txt",request.FILES["taskFile"])
            task.save()
        else:
            json = getJson({"flag":"no"})
    except BaseException as e:
        print e
        json = getJson({"flag":"no"})
    return HttpResponse(json)
def delTask(request):
    try:
        if request.POST.get("id"):
            task = ContentTask.objects.get(id=int(request.POST["id"]))
            task.delete()
        else:
            json = getJson({"flag":"no"})
        json = getJson({"flag":"yes"})
    except BaseException:
        json = getJson({"flag":"no"})
    return HttpResponse(json)
def taskEditPre(request,id):
    try:
        task = ContentTask.objects.get(id=int(id))
    except BaseException:
        return Http404()
    return consoleRender(r"adminConsole"+os.path.sep+"task"+os.path.sep+"taskEdit.html",{"task":task},request)
def taskEdit(request):
    try:
        task = ContentTask.objects.get(id=int(request.POST["id"]))
        task.taskType,task.taskName = int(request.POST["taskType"]),request.POST["taskName"]
        if len(request.FILES):
            task.fileName.delete()
            task.fileName.save("TXT_"+str(uuid.uuid1())+".txt",request.FILES["taskFile"])
        task.save()
        json = getJson({"flag":"yes"})
    except BaseException as e:
        json = getJson({"flag":"no"})
    return HttpResponse(json)
def taskUpdate(request):
    try:
        task = ContentTask.objects.get(id=int(request.POST["id"]))
        if task.processFlag == "Prepare":
            task.processFlag ="Start"
            task.startTs = datetime.datetime.now()
            task.save()
        json = getJson({"flag":"yes"})
    except BaseException as e:
        json = getJson({"flag":"no"})
    return HttpResponse(json)


