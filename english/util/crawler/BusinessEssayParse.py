# --*-- coding:utf-8 --*--
import datetime
import os
import uuid
from django.core.files.base import ContentFile
from english.video.models import OpenCourse, CourseDetail
from english.article.models import BusinessEssay

if 'SERVER_SOFTWARE' in os.environ:
    from english.article.models import BusinessEssay

__author__ = 'Administrator'

from pyquery import PyQuery as pq
def feedBusiness():
    urls = []
    urls.append("http://www.hxen.com/englishlistening/businessenglish/zhichangshejiao/index.html")
    urls.append("http://www.hxen.com/englishlistening/businessenglish/zhichangshejiao/index_2.html")
    urls.append("http://www.hxen.com/englishlistening/businessenglish/zhichangshejiao/index_3.html")
    #文件链接
    articleUrl = []
    for url in urls:
        d = pq(url=url)
        tag_a = d(".leftList ul li a")
        for alink in tag_a:
            articleUrl.append("http://www.hxen.com"+d(alink).attr("href"))
    #处理文章
    for link in articleUrl:
        art = pq(url=link)
        bus = BusinessEssay()
        bus.displayName = art("h1").text()
        bus.category='职场社交'
        bus.tag='职场'
        content =''
        content_p = art("#arctext p")
        for x in range(6,len(content_p)):
            if art(content_p[x]).attr("class") == 'MsoN.mp3al' and len(art(content_p[x]).text()):
                content +="<p>"+art(content_p[x]).text() +"</p>"
        bus.content = content
        bus.createDate = datetime.datetime.now()
        bus.save()

def business300():
    #http://www.hxen.com/englishlistening/businessenglish/shangwu1/
    urls = []
    urls.append("http://www.hxen.com/englishlistening/businessenglish/negotiation/")
    #文件链接
    articleUrl = []
    for url in urls:
        d = pq(url=url)
        tag_a = d(".leftList ul li a")
        for alink in tag_a:
            articleUrl.append("http://www.hxen.com"+d(alink).attr("href"))
        #处理文章
    for link in articleUrl:
        art = pq(url=link)
        bus = BusinessEssay()
        bus.displayName = art("h1").text()
        bus.category='商务谈判'
        bus.tag='谈判技巧'
        content =''
        content_p = art("#arctext p")
        for x in range(0,len(content_p)):
            if len(art(content_p[x]).text()):
                content +="<p>"+art(content_p[x]).text() +"</p>"
        bus.content = content
        bus.createDate = datetime.datetime.now()
        bus.save()
import chardet
import urllib2 as urllib
def course():
    datal = urllib.urlopen("http://open.163.com/ocw/").read()
    top =pq(datal.decode("GB2312").encode("utf-8"))
    cour = {}
    courImg = {}
    for section in top(".m-t-bg"):
        topC = pq(section)
        #大类标题
        cour[topC("h2").text()] = {}
        courImg[topC("h2").text()] = {}
        print topC("h2").text()
        for sc in topC(".m-conmt"):
            scTitle = pq(sc)
            cour[topC("h2").text()][scTitle("h3").text()] = []
            for href in scTitle(".cimg"):
                courImg[topC("h2").text()][scTitle("h3").text()]=scTitle(href).children("img").attr("data-original")
                cour[topC("h2").text()][scTitle("h3").text()].append(scTitle(href).attr("href"))
    for key in cour:
        print key
        for k2 in cour[key]:
            print '---------',k2
            for ak in cour[key][k2]:
                saveCourse(key,k2,ak,courImg[key][k2])
def saveCourse(cate,branch,url,photo):
    mycourse = OpenCourse()
    coursedata = urllib.urlopen(url).read()
    #body开始
    htmlContent =coursedata
    bodySt =htmlContent.find("<body>")
    bodyEnd =htmlContent.find("</body>")+7
    body = htmlContent[bodySt:bodyEnd]
    print chardet.detect(body)
    top = pq(body.decode("GB2312"))
    title = top(".m-cdes h2")[0]
    introduce = top(".m-cdes p")[2]
    school = top(".cContent")[0]
    clis = top("#list1 .u-ctitle")
    print '标题',top(title).text()
    mycourse.title = top(title).text()
    print "教室",top(".picText").text()
    mycourse.teacher =top(".picText").text()
    print '介绍',top(introduce).text(),
    mycourse.introduce = top(introduce).text()
    print '学校',top(school).text()
    mycourse.schoolName = top(school).text()
    mycourse.category = branch
    mycourse.topCategory =cate
    mycourse.updateTs = datetime.datetime.now()
    print '下图',photo
    mycourse.smallImage.save(str(uuid.uuid1())+".jpg",ContentFile(urllib.urlopen(photo).read()))
    print '大图',top(".m-cintro").children("img").attr("src")
    mycourse.largeImage.save(str(uuid.uuid1())+".jpg",ContentFile(urllib.urlopen(top(".m-cintro").children("img").attr("src")).read()))
    print '教师图',top(".picText").children("img").attr("src")
    if top(".picText").children("img").attr("src"):
        mycourse.teacherPhoto.save(str(uuid.uuid1())+".jpg",ContentFile(urllib.urlopen(top(".picText").children("img").attr("src")).read()))
    mycourse.save()
    order = 0
    for x in clis:
        order += 1
        detail = CourseDetail()
        print top(x).text()
        detail.title = top(x).text()
        detail.orders = order
        if len(top(x).parent().children(".u-cdown").children("a")):
            detail.translated = True
            print top(x).parent().children(".u-cdown a").attr("href")
            detail.videoUrl = top(x).parent().children(".u-cdown a").attr("href")
        else:
            detail.translated = False
        detail.courseId = mycourse
        detail.save()
    #课程