# --*-- coding:utf-8 --*--
import os
from django.db import models
## 注册用户
# 注册用户
class StudyUser(models.Model):
    GENDER=(("男",1),("女",0))
    userName = models.CharField(max_length=50,verbose_name="用户名")
    nickName = models.CharField(max_length=50,verbose_name="昵称")
    passwords = models.CharField(max_length=32,verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱地址")
#    gender = models.IntegerField(choices=GENDER)
#    age = models.IntegerField(min=1,max=120)
#    birthday = models.DateField()
    photo = models.ImageField(upload_to="photos")
    thirdType = models.IntegerField(verbose_name="第三方类型")
    thirdId = models.CharField(max_length=10,verbose_name="第三方id")
    thirdKey = models.CharField(max_length=50,verbose_name="KEY")
    thirdScrite = models.CharField(max_length=50,verbose_name="Se")
    regDate = models.DateField()