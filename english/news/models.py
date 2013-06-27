# --*-- coding:utf-8 --*--
from django.db import models
import datetime

class News(models.Model):
    #内容类型
    CONTENT_TYPE = (
        (1, '文章'),
        (2, '图文'),
        (3, '分页'),
        (4, '其他'),
    )
    TAG={"sports":'体育',"entertainment":'娱乐',"politics":"时政","campus":"校园","life":"生活","economy":"经济","tech":"科技","career":"职场"}
    UNTAG={'体育':"sports",
           '娱乐':"entertainment",
           "时政":"politics",
           "校园":"campus",
           "生活":"life",
           "经济":"economy",
           "科技":"tech",
           "职场":"career"}
    title = models.CharField(max_length=100,verbose_name="新闻标题")
    titleEnglish=models.CharField(max_length=100,verbose_name="英文标题")
    introduce = models.TextField(verbose_name="导读",)
    content = models.TextField(verbose_name="中文内容")
    contentEnglish = models.TextField(verbose_name="英文内容")
    hot = models.BooleanField(verbose_name="是否热点")
    readCount = models.IntegerField(verbose_name="阅读数量",default=0)
    shareCount = models.IntegerField(verbose_name="分享数量",default=0)
    comeFrom = models.CharField(max_length=200,verbose_name="来源")
    contentType = models.IntegerField(choices=CONTENT_TYPE,verbose_name="内容类型",default=2)
    tags = models.CharField(max_length=200,verbose_name="标签")
    categroy = models.ForeignKey("NewsCategory",blank=True)
    # imageShow = models.ImageField(verbose_name="插图",upload_to="newsImg",blank=True)
    commentCount = models.IntegerField(verbose_name="评论数",default=0)
    # lastUpdateFlag = models.IntegerField(default=0)
    versions = models.IntegerField(blank=True)
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
        super(News, self).save(*args, **kwargs)
    def delete(self, using=None):
        for res in self.newsres_set.all():
            res.delete()
        super(News,self).delete()
class NewsCategory(models.Model):
    typeName = models.CharField(max_length=10)
    typeUrl = models.CharField(max_length=20)
    typeOrder = models.IntegerField(default=0)
    categoryDesc = models.TextField(blank=True)
class NewsRes(models.Model):
    resUrl = models.ImageField(upload_to="newsImage")
    newsId = models.ForeignKey("News")
    def delete(self, using=None):
        from english.util.storagetool import delFile
        delFile(self.resUrl.name)
        models.Model.delete(self)
class Comment(models.Model):
    user = models.ForeignKey("studyuser.StudyUser")
    message = models.CharField(max_length=200)
    news = models.ForeignKey('News')
    ipAddr = models.CharField(max_length=20)
    ipName = models.CharField(max_length=50)
    agreeWith = models.IntegerField(default=0)
    followPid = models.ForeignKey('self',null = True, blank = True)
    createTs = models.DateTimeField()
#i = 1
#for x in News.TAG:
#    cate = NewsCategory()
#    cate.typeUrl = x
#    cate.typeName = News.TAG[x]
#    cate.categoryDesc = News.TAG[x]
#    cate.typeOrder = i
#    cate.save()
#    i += 1