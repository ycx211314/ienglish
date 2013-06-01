# --*-- coding:utf-8 --*--
__author__ = 'Prince'
import os
from django.db import models
import datetime
#公开课
class OpenCourse(models.Model):
    title = models.CharField(max_length=100)   #标题
    introduce = models.TextField()   #简介
    schoolName = models.TextField()        #学院简介
    teacher = models.TextField(blank=True)  #讲师简介
    teacherPhoto = models.ImageField(upload_to="course",blank=True)       #讲师头像
    smallImage = models.ImageField(upload_to="course")     #小图
    largeImage = models.ImageField(upload_to="course")      #大图   a
    allVideoUrl = models.URLField(blank=True) #全部打包地址
    topCategory = models.CharField(max_length=20)
    category = models.CharField(max_length=10)
    updateTs = models.DateTimeField()
#详细课程
class CourseDetail(models.Model):
    title = models.CharField(max_length=200)
    courseId = models.ForeignKey("OpenCourse")
    orders = models.IntegerField(default=0)
    translated = models.BooleanField(default=False)
    videoCode = models.TextField(blank=True)
    videoUrl = models.URLField(blank=True)
    pass