# --*-- coding:utf-8 --*--
__author__ = 'Prince'
import os
from django.db import models
import datetime
#公开课
class OpenCourse(models.Model):
    title = models.CharField(max_length=50)   #标题
    introduce = models.TextField()   #简介
    schoolName = models.TextField()        #学院简介
    teacher = models.TextField()  #讲师简介
    teacherPhoto = models.ImageField()       #讲师头像
    smallImage = models.ImageField()     #小图
    largeImage = models.ImageField()      #大图   a
    allVideoUrl = models.URLField() #全部打包地址
    updateTs = models.DateTimeField()
    pass