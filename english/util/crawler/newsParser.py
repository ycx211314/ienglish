# --*-- coding:utf-8 --*--
import codecs

__author__ = 'Administrator'
from pyquery import PyQuery as pq

def newParser(baseUrl,filename,page):
    urls = []
    #urls.append("http://www.i21st.cn/story/index_Tech_18.html")
#    for x in range(1,page):
#        #urls.append("http://www.i21st.cn/story/index_Tech_"+str(x)+".html")
#        urls.append(baseUrl+str(x)+".html")
    urls.append("http://www.i21st.cn/story/index_Tech.html")
    #文件链接
    articleUrl = []
    for url in urls:
        d = pq(url=url)
        tag_a = d(".Table1 span[class='ft-gray']").parent()
        for alink in tag_a:
            articleUrl.append("http://www.i21st.cn"+d(alink).attr("href"))
        #处理文章
    articleUrl.append("http://www.i21st.cn/story/1873.html")
    print len(articleUrl)
    eng = codecs.open(filename,"a","utf-8")
    for link in articleUrl:
        try:
            cont = pq(url = link)
        except:
            print "----------------------",link
        eng.write("START\r\n")
        eng.write("EN:"+cont("h1").text()+"\r\n")
        eng.write("CH:"+cont("h2").text()+"\r\n")
        fx = cont(".extinfo .author").html().encode("utf-8")
        eng.write("TS:"+fx[0:10]+"\r\n")
        eng.write("SH:"+cont(".introduction").text()+"\r\n")
        contentEn = ""
        for contEn in cont(".story_en"):
            contentEn += cont(contEn).text()+"|||"
        eng.write(u"MC:"+contentEn+"\r\n")
        contentCH = ""
        for contCH in cont(".story_cn"):
            contentCH += cont(contCH).text()+"|||"
        eng.write(u"MH:"+contentCH+"\r\n")
        imgUrl = ""
        for img in cont("img[longdesc]"):
            imgUrl +="http://www.i21st.cn"+cont(img).attr("longdesc")+"|||"
        eng.write(u"IM:"+imgUrl+"\r\n")
        eng.write(u"END"+"\r\n")
        print link
    eng.close()
newParser("http://www.i21st.cn/story/index_Tech_","tech.txt",19)
#newParser("http://www.i21st.cn/story/index_Politics_","poli.txt",5)
#newParser("http://www.i21st.cn/story/index_Edu_","edu.txt",16)
#newParser("http://www.i21st.cn/story/index_Lifestyle_","life.txt",40)
#newParser("http://www.i21st.cn/story/index_Ent_","ent.txt",35)
#newParser("http://www.i21st.cn/story/index_Sports_","sport.txt",3)
#newParser("http://www.i21st.cn/story/index_Economy_","econ.txt",7)
#newParser("http://www.i21st.cn/story/index_Career_","career.txt",5)

