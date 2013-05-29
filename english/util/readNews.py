# --*-- coding:utf-8 --*--
import datetime
import uuid
from django.core.files.base import ContentFile
from english.news.models import News
from english.util.newsParser import F21stParse

__author__ = 'Administrator'
import urllib2
import re
class ReadNewsFrom21():
    def __init__(self,baseUrl,rege,rootUrl=''):
        self.baseUrl = baseUrl
        self.rege = rege
        self.rootUrl = rootUrl
        curNow = datetime.datetime.now()
        if len(News.objects.all()):
            lastDate = News.objects.order_by("-createDate")[0].createDate
            if lastDate.year == curNow.year and lastDate.month == curNow.month and lastDate.day ==curNow.day:
                self.flag = False
            else:
                self.flag = True
        else:
            self.flag =True
    def extract_url(self):
        content = urllib2.urlopen(self.baseUrl).read()
        reg_url = re.findall(self.rege,content)
        self.reg_url = sorted(set(reg_url),reverse=True)
        return self.reg_url
    def feedMsg(self):
        if not self.flag:
            return
        for sub_url in self.extract_url():
            newsParser = F21stParse()
            if str(sub_url).find(self.baseUrl) == -1:
                 sub_web = urllib2.urlopen(self.rootUrl + sub_url).read()
            else:
                sub_web = urllib2.urlopen(sub_url).read()
            newsParser.feed(sub_web)
            news = News()
            news.hot = False
            news.title = newsParser.title
            news.titleEnglish = newsParser.titleEnglish
            for cont in newsParser.content:
                if not len(cont):
                    continue
                news.content = news.content + "###" + cont
            for cont in newsParser.contentEn:
                if not len(cont):
                    continue
                news.contentEnglish = news.contentEnglish +"###"+ cont
            news.comeFrom = newsParser.author[1]
            news.introduce = newsParser.introduction
            news.imageShow.save(str(uuid.uuid1())+".jpg",ContentFile(urllib2.urlopen(self.rootUrl+newsParser.imageUrl).read()));
            news.save()