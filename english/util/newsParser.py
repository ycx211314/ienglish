# --*-- coding:utf-8 --*--
__author__ = 'Administrator'
from HTMLParser import HTMLParser
#http://www.i21st.cn 双语新闻处理
class F21stParse(HTMLParser):
    def __init__(self):
        self.title='' #标题
        self.titleEnglish='' #英语标题
        self.introduction = ''
        self.author = []
        self.content = []    #内容
        self.contentEn=[] #english内容
        self.imageUrl = ""
        """ 处理标记 """
        self.titleFlag = False #标题内容开始
        self.titleEnFlag = False #英文标题开始
        self.startContent = False #处理内容标记
        self.isContent = False  #内容开始,英文true,中文FALSE
        self.isContentEn = False #英文内容处理
        self.contentTag = "div"  #内容标记标签
        self.tag = "" #当前处理标签
        self.introTag = False
        self.handleTag =""
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        self.tag = tag
        if tag == "h1":
            self.titleEnFlag =True
        if tag =="h2": #处理中文标题
            self.titleFlag = True
        if tag == "div" and ('id',"storyBody") in attrs:      #处理内容开始
            self.startContent = True
            self.contentTag = tag
        if tag =="span" and ('class','story_en txt-14 ft-blue') in attrs: #处理ying文内容
            self.isContent = True
        if tag =="span" and ('class','story_cn txt-14') in attrs: #处理中文内容
            self.isContentEn = True
        if tag == "img" and "longdesc" in dict(attrs).keys():
            self.imageUrl = dict(attrs).get("longdesc")
        if tag == "div" and ("class","txt-12 ft-dark") in attrs:
            self.introTag = True
        if tag == "span" and ("class","author") in attrs:
            self.handleTag = "author"
    def handle_data(self, data):
        #标题
        if self.titleFlag:
            self.title = data
        if self.titleEnFlag:
            self.titleEnglish = data
        if self.handleTag == "author":
            self.author.append(data)
        #内容处理
        if self.startContent:
            if self.isContent:
                self.content.append(unicode(data,"utf-8"))
            elif self.isContentEn:
                self.contentEn.append(unicode(data,"utf-8"))
        if self.introTag:
            self.introduction = data
    def handle_endtag(self, tag):
        self.titleFlag = False
        self.titleEnFlag = False
        self.isContent = False
        self.isContentEn = False
        self.introTag = False
        self.handleTag =""
        if self.tag == self.contentTag:
            self.startContent = False
            self.introTag = False
    def handle_startendtag(self, tag, attrs):
        print tag