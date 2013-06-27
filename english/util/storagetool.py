# --*-- coding:utf-8 --*--
__author__ = 'Administrator'
from sae.storage import Bucket
def uploadFile(filename,file,contentTyp):
    bucket = Bucket('files')
    bucket.put_object(filename,file,contentTyp,"uft-8")
    pass
def delFile(filename):
    bucket = Bucket('images')
    bucket.delete_object(filename)
    return True