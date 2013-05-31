# --*-- coding:utf-8 --*--
import re

__author__ = 'Administrator'
urlConfigs = {
    r"^/$": 1,
    r"/news/\.?": 2,
    r"/read/\.?": 3,
    }
class Nav:
    def __init__(self):
        self.navTop = 1
        self.left = 1
    pass
def urlMatch(path):
    nav = Nav()
    for key, value in urlConfigs.iteritems():
        pattern = re.compile(key)
        if pattern.match(path):
            nav.navTop = value
            break
    return nav