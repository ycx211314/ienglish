# Create your views here.
# --*-- coding:utf-8 --*--
import datetime,os
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response

#跳转到主页
from django.template import RequestContext
from english.news.encoder import getJson
from english.studyuser.models import StudyUser
import re
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
def regPre(request):
    return render_to_response(r'studyuser'+os.path.sep+'regist.html',context_instance=RequestContext(request))
#注册操作
def reg(request):
    if request.method == 'POST':
        user = StudyUser();
        try:
            user.passwords =  request.POST['password'];
            user.userName =  request.POST['userName'];
            user.email = request.POST['email'];
            user.nickName = request.POST['nickName'];
            user.regDate = datetime.datetime.now().strftime('%Y-%m-%d')
            if len(user.email) < 1:
                raise  Exception(' 邮箱不合法');
            if len(user.nickName) < 1 or len(user.nickName) > 50:
                raise  Exception(' 昵称长度不合法');
            if len(user.passwords) < 6 or len(user.passwords) > 32:
                raise  Exception(' 密码长度不合法');
            if len(user.userName) < 6 or len(user.userName) > 50:
                raise  Exception(' 用户名长度不合法');
            tempuser= StudyUser.objects.filter(userName=user.userName)
            if len(tempuser) > 0:
                raise Exception('用户名已被使用')
            user.thirdType = 1
            user.thirdId = '1';
            user.third = '1';
            user.thirdScrite = '1';
            StudyUser.save(user);
        except Exception , e:
            return render_to_response(r'forward.html',{"alertMessage":"注册失败:"+e.message,"redirectUrl":r"/user/registerpre/"});
        return render_to_response(r'forward.html',{"alertMessage":"注册成功！","redirectUrl":"/index/"});
    else:
        return render_to_response(r'forward.html',{"alertMessage":"哥们别逗了，正经注册去~~！","redirectUrl": r"/user/registerpre/"});                                                                               q
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
