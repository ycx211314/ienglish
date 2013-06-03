# --*-- coding:utf-8 --*--
from django.db import models
import datetime

class News(models.Model):
    title = models.CharField(max_length=100,verbose_name="新闻标题")
    titleEnglish=models.CharField(max_length=100,verbose_name="英文标题")
    introduce = models.CharField(max_length=300,verbose_name="导读")
    content = models.TextField(verbose_name="中文内容")
    contentEnglish = models.TextField(verbose_name="英文内容")
    hot = models.BooleanField(verbose_name="是否热点")
    readCount = models.IntegerField(verbose_name="阅读数量",default=0)
    shareCount = models.IntegerField(verbose_name="分享数量",default=0)
    comeFrom = models.CharField(max_length=200,verbose_name="来源")
    imageShow = models.ImageField(verbose_name="插图",upload_to="newsImg")
    commentCount = models.IntegerField(verbose_name="评论数",default=0)
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
        self.shareCount = 0
        self.createDate = datetime.datetime.now()
        super(News, self).save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey("studyuser.StudyUser")
    message = models.CharField(max_length=200)
    news = models.ForeignKey('News')
    ipAddr = models.CharField(max_length=20)
    ipName = models.CharField(max_length=50)
    agreeWith = models.IntegerField(default=0)
    followPid = models.ForeignKey('self',null = True, blank = True)
    createTs = models.DateTimeField()