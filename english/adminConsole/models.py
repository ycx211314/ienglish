# --*-- coding:utf-8 --*--
__author__ = 'Administrator'
from django.db import models
class Menu(models.Model):
    TARGET=(
        ("新页面","_blank"),
        ("当前页","_self"),
        ("父页面","_parent"),
        ("顶端页","_top"),
    )
    displayName = models.CharField(max_length=100)
    target = models.CharField(max_length=10,default="_self")
    href = models.CharField(max_length=200)
    show = models.BooleanField(default=True)
    level = models.IntegerField(default=0)
    iconCls = models.CharField(max_length=50,blank=True)
    parent = models.ForeignKey('self',null = True, blank = True)

    def __unicode__(self):
        return self.displayName
