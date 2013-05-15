# --*-- coding:utf-8 --*--
from HTMLParser import HTMLParser
import datetime
import re
from threading import Thread
import urllib2
from english.article.models import ShortArticel

__author__ = 'Administrator'

class ArticleParse(HTMLParser):
    def __init__(self):
        self.title = '' #标题
        self.titleEnglish = '' #英语标题
        self.author = []
        self.content = []    #内容
        """ 处理标记 """
        self.titleFlag = False #标题内容开始
        self.startContent = False #处理内容标记
        self.isContent = False  #内容开始,英文true,中文FALSE
        self.tag = "" #当前处理标签
        self.handleTag = ""
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.tag = tag
        if tag == "div" and ("class","content_txt") in attrs:
            self.startContent = True
        if tag =="div" and ("class","pages") in attrs:
            self.startContent = False
        if tag =="h1":
            self.titleFlag = True
        if tag =="p" and  self.startContent:
            self.isContent = True
        pass

    def handle_endtag(self, tag):
        self.titleFlag = False
        self.isContent = False
        self.handleTag =""

    def handle_data(self, data):
        #标题
        if self.titleFlag:
            self.title = unicode(data,"gb2312")[7:]
        #内容处理
        if self.startContent:
            if len(unicode(data,"gb2312").strip()) > 1:
                self.content.append(unicode(data,"gb2312").strip())
    pass
class ReadArticle:
    def __init__(self, baseUrl, rege, rootUrl=''):
        self.baseUrl = baseUrl
        self.rege = rege
        self.rootUrl = rootUrl
        self.flag = True

    def extract_url(self):
        content = urllib2.urlopen(self.baseUrl).read()
        reg_url = re.findall(self.rege, content)
        self.reg_url = sorted(set(reg_url), reverse=True)
        return self.reg_url
    def feedMsg(self):
        if not self.flag:
            return
        for sub_url in self.extract_url():
            parser = ArticleParse()
            if str(sub_url).find(self.baseUrl) == -1:
                sub_web = urllib2.urlopen(self.rootUrl + sub_url).read()
            else:
                sub_web = urllib2.urlopen(sub_url).read()
            parser.feed(sub_web)
            newArticel = ShortArticel()
            startEn = False
            startCh = False
            contentEn = ''
            contentCh = ''
            for cont in parser.content:
                if cont == unicode('[美文欣赏]',"utf-8"):
                    startEn = True
                    startCh = False
                    continue
                elif cont ==unicode( '[参考译文]',"utf-8"):
                    startCh = True
                    startEn = False
                    continue
                if startEn:
                    contentEn = contentEn + cont +"<br>"
                elif startCh:
                    contentCh =contentCh + cont +"<br>"
            newArticel.displayName = parser.title
            newArticel.content = contentEn
            newArticel.contentCH = contentCh
            newArticel.createDate = datetime.date.today()
            newArticel.save()
           # print parser.title,"----",contentEn,"\r\n"
           # print contentCh
#            news = News()
#            news.hot = False
#            news.title = newsParser.title
#            news.titleEnglish = newsParser.titleEnglish
#            for cont in newsParser.content:
#                if not len(cont):
#                    continue
#                news.content = news.content + "###" + cont
#            for cont in newsParser.contentEn:
#                if not len(cont):
#                    continue
#                news.contentEnglish = news.contentEnglish + "###" + cont
#            news.comeFrom = newsParser.author[1]
#            news.introduce = newsParser.introduction
#            news.imageShow.save(str(uuid.uuid1()) + ".jpg",
#                ContentFile(urllib2.urlopen(self.rootUrl + newsParser.imageUrl).read()));
#            news.save()
    #