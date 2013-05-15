# --*-- coding:utf-8 --*--
from django.db import models

# 资源信息
class Resource(models.Model):
    displayName = models.CharField(max_length=100)
    pointCount = models.IntegerField(default=0)
    createDate = models.DateField()
    pass
# 精美短文
class ShortArticel(Resource):
    englishTitle = models.CharField(max_length=100,blank=True)
    content = models.TextField()
    contentCH = models.TextField()
    images = models.ImageField(upload_to="resimg",blank=True)
    read = models.BooleanField()
    source = models.FileField(upload_to="audio",blank=True)
    def __unicode__(self):
        return self.displayName
    class Meta:
        get_latest_by = "-createDate"
        verbose_name = '精美短文'
        verbose_name_plural = "精美短文"
    pass
#class Video(Resource):
#    pass
#class Audio(Resource):
#    pass
