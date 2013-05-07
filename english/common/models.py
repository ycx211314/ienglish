# --*-- coding:utf-8 --*--
import os
from django.db import models
from english import settings
import datetime

class News(models.Model):
    title = models.CharField(max_length=100,verbose_name="新闻标题")
    titleEnglish=models.CharField(max_length=100,verbose_name="英文标题")
    introduce = models.CharField(max_length=300,verbose_name="导读")
    content = models.TextField(verbose_name="中文内容")
    contentEnglish = models.TextField(verbose_name="英文内容")
    hot = models.BooleanField(verbose_name="是否热点")
    readCount = models.IntegerField(verbose_name="阅读数量",default=0)
    comeFrom = models.CharField(max_length=200,verbose_name="来源")
    imageShow = models.ImageField(verbose_name="插图",upload_to="newsImg")
    lastUpdateFlag = models.IntegerField(default=0)
    createDate = models.DateTimeField()
    class Meta:
        get_latest_by = "-createDate"
        verbose_name = '双语新闻'
        verbose_name_plural = "双语新闻"
    def __unicode__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.readCount = 0
        self.createDate = datetime.datetime.now()
        super(News, self).save(*args, **kwargs)


# 注册用户
class StudyUser(models.Model):
    userName = models.CharField(max_length=50,verbose_name="用户名")
    nickName = models.CharField(max_length=50,verbose_name="昵称")
    passwords = models.CharField(max_length=32,verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱地址")
    photo = models.ImageField(upload_to="photos")
    thirdType = models.IntegerField(verbose_name="第三方类型")
    thirdId = models.CharField(max_length=10,verbose_name="第三方id")
    thirdKey = models.CharField(max_length=50,verbose_name="KEY")
    thirdScrite = models.CharField(max_length=50,verbose_name="Se")
    regDate = models.DateField()