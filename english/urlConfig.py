# --*-- coding:utf-8 --*--
import re

__author__ = 'Administrator'
urlConfigs = {
    "/":1,
    "/news/\.?":2,
    }
class Nav:
    def __init__(self):
        self.navTop = 1
        self.left = 1
    pass
def urlMatch(path):
    nav = Nav()
    for key,value in urlConfigs.iteritems():
        pattern = re.compile(key)
        if pattern.match(path):
            nav.navTop = value
    return nav