# Create your views here.
# --*-- coding:utf-8 --*--
import datetime
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response

#跳转到主页
from django.template import RequestContext
from english.news.encoder import getJson
from english.studyuser.models import StudyUser
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
#注册前信息查询
def RegPre(request):
    return render_to_response(r'studyuser\regist.html',context_instance=RequestContext(request))
def Reg(request):
    user = StudyUser();
    user.passwords =  request.POST['password'];
    user.userName =  request.POST['userName'];
    user.email = request.POST['email'];
    user.nickName = request.POST['nickName'];
    #user.photo = request.POST['photo']
    user.thirdType = 1
    user.thirdId = '1';
    user.third = '1';
    user.thirdScrite = '1';
    user.regDate = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        StudyUser.save(user);
    except RuntimeError:
        return render_to_response(r'forward.html',{"alertMessage":"注册失败，请重新注册","redirectUrl":"/index/"});
    return render_to_response(r'forward.html',{"alertMessage":"注册成功","redirectUrl":"/index/"});

def userExsit(request,name):
    try:
        username = name
    except:
        return HttpResponse(getJson({"flag":"no"}))
    users = StudyUser.objects.filter(userName=username).all()
    if len(users):
        return HttpResponse(getJson({"flag":"no"}))
    else:
        return HttpResponse(getJson({"flag":"ok"}))
