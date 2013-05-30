# --*-- coding:utf-8 --*--
# __author__ = 'Administrator'
import sched, time
from threading import Thread, Timer
from english.util.crawler.ArticleParse import ReadArticle
from english.util.crawler.BusinessEssayParse import *
from english.util.readNews import ReadNewsFrom21
class NewsTask(Thread):
    def run(self):
        reader = ReadNewsFrom21(baseUrl="http://www.i21st.cn/story/index.html",rege="/story/\d{4}.html",rootUrl="http://www.i21st.cn")
        reader.feedMsg()
class ArticleTask(Thread):
    def run(self):
        reader = ReadArticle(baseUrl="http://www.yingyu.com/dx/zuowen/yymwxs/",rege="/e/\d{8}/4d\w{11}.shtml",rootUrl="http://www.yingyu.com")
        reader.feedMsg()
class BusinessTask(Thread):
    def run(self):
        feedBusiness()
        #business300()
#s = sched.scheduler(time.time, time.sleep)
#
#class Job(Thread):
#    def run(self):
#        print "this is start Taks"
#
#def each_day_time(hour, min, sec, next_day=True):
#    '''返回当天指定时分秒的时间'''
#    struct = time.localtime()
#    if next_day:
#        day = struct.tm_mday + 1
#    else:
#        day = struct.tm_mday
#    return time.mktime((struct.tm_year, struct.tm_mon, day,
#                        hour, min, sec, struct.tm_wday, struct.tm_yday,
#                        struct.tm_isdst))
#
#def print_time(name="None"):
#    print name, ":", "From print_time",\
#    time.time(), " :", time.ctime()
#
#def do_somthing():
#    job = Job()
#    job.start()
#def echo_start_msg():
#    print "-------------- auto compile begin running --------------"
#def main():
##指定时间点执行任务
#    s.enterabs(each_day_time(1, 0, 0, True), 1, echo_start_msg, ())
#s.run()
#while (True):
#    Timer(0, do_somthing, ()).start()
#time.sleep(24 * 60 * 60)