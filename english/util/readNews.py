# --*-- coding:utf-8 --*--
import codecs
import datetime
import uuid,os
#from django.core.files.base import ContentFile
#from english.news.models import News
#from english.util.newsParser import F21stParse
from django.core.files.base import ContentFile
from english.news.models import NewsRes, News,NewsCategory

if 'SERVER_SOFTWARE' in os.environ:
    import sae.storage
__author__ = 'Administrator'
import urllib2
from english.settings import MEDIA_ROOT
def readNewsFromText():
    count = 0
    path = MEDIA_ROOT+os.path.sep+"newsText"
    for files in os.listdir(path):
        if os.path.isfile(os.path.join(path,files)) and os.path.splitext(files)[1] =='.txt':
            with codecs.open(os.path.join(path,files)) as file:
                types = file.readline()
                categroy = NewsCategory.objects.get(typeName=types[0:len(types)-2])
                while True:
                    content = file.readline()
                    if len(content):
                        content = content[0:len(content)-2]
                        if str(content).startswith("START"):
                            curNews = News()
                            curNews.comeFrom="21st "
                            curNews.contentType = 2
                            if categroy:
                                curNews.categroy = categroy
                            curNews.tags=""
                            print 'create new vo'
                        if str(content).startswith("EN:"):
                            curNews.titleEnglish = content[3:]
                        if str(content).startswith("CH:"):
                            curNews.title = content[3:]
                        if str(content).startswith("TS:"):
                            curNews.createDate = datetime.datetime.strptime(content[3:], '%Y-%m-%d')
                        if str(content).startswith("SH:"):
                            curNews.introduce = content[3:]
                        if str(content).startswith("MC:"):
                            curNews.contentEnglish = content[3:]
                        if str(content).startswith("MH:"):
                            curNews.content = content[3:]
                        if str(content).startswith("IM:"):
                            imageUrl = str(content[3:]).split("|||")
                        if str(content).startswith("END"):
                            count +=1
                            print curNews.title
                            print curNews.introduce
                            curNews.save()
                            for imgurl in imageUrl:
                                if len(imgurl):
                                    newsres = NewsRes()
                                    newsres.newsId =curNews
                                    try:
                                        newsres.resUrl.save("IMG_"+str(categroy.id)+str(uuid.uuid1())+".jpg",ContentFile(urllib2.urlopen(imgurl).read()))
                                        newsres.save()
                                    except urllib2.HTTPError:
                                        continue
                            print 'save vo'
                    else:
                        break
            os.remove(os.path.join(path,files))
    print count
#
#
#
#
#class ReadNewsFrom21():
#    def __init__(self,baseUrl,rege,rootUrl=''):
#        self.baseUrl = baseUrl
#        self.rege = rege
#        self.rootUrl = rootUrl
#        curNow = datetime.datetime.now()
#        if len(News.objects.all()):
#            lastDate = News.objects.order_by("-createDate")[0].createDate
#            if lastDate.year == curNow.year and lastDate.month == curNow.month and lastDate.day ==curNow.day:
#                self.flag = False
#            else:
#                self.flag = True
#        else:
#            self.flag =True
#    def extract_url(self):
#        content = urllib2.urlopen(self.baseUrl).read()
#        reg_url = re.findall(self.rege,content)
#        self.reg_url = sorted(set(reg_url),reverse=True)
#        return self.reg_url
#    def feedMsg(self):
#        if not self.flag:
#            return
#            # 初始化一个Storage客户端。
#        if 'SERVER_SOFTWARE' in os.environ:
#            s = sae.storage.Client()
#        for sub_url in self.extract_url():
#            newsParser = F21stParse()
#            if str(sub_url).find(self.baseUrl) == -1:
#                 sub_web = urllib2.urlopen(self.rootUrl + sub_url).read()
#            else:
#                sub_web = urllib2.urlopen(sub_url).read()
#            newsParser.feed(sub_web)
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
#                news.contentEnglish = news.contentEnglish +"###"+ cont
#            news.comeFrom = newsParser.author[1]
#            news.introduce = newsParser.introduction
#            news.contentType = 1
#            if 'SERVER_SOFTWARE' in os.environ:
#                ob = sae.storage.Object(urllib2.urlopen(self.rootUrl+newsParser.imageUrl).read(),content_type='image/jpeg')
#                imgName = str(uuid.uuid1())+".jpg"
#                s.put('english',imgName, ob)
#                news.imageShow.name = imgName
#            else:
#                news.imageShow.save(str(uuid.uuid1())+".jpg",ContentFile(urllib2.urlopen(self.rootUrl+newsParser.imageUrl).read()))
#            news.save()