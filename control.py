# -*- coding:UTF8 -*-

import os
import threading
import traceback
import json
import time
import urllib
import random
import sys
import subprocess
from PyQt4 import QtNetwork
from PyQt4 import QtWebKit
from PyQt4 import QtCore


class Control(QtCore.QThread):
            
    doSignal = QtCore.pyqtSignal()
    logSignal = QtCore.pyqtSignal(str)
    restartSignal = QtCore.pyqtSignal()
    defaultCommentList = [u"秒赞！"]
    def __init__(self,networkAccessManager, uin, gtk, config):
        super(Control, self).__init__()
        
        self.errorLogPath = "error.txt"
        self.workFinished = True
        self.__config = config
        self.config = config.get(uin)
        self.uin = uin
        self.gtk = gtk
        self.page = QtWebKit.QWebPage()
        self.webFrame = self.page.mainFrame()
        self.running = False
        self.networkAccessManager = networkAccessManager
#        self.networkAccessManager = QtNetwork.QNetworkAccessManager(self)
#        self.cookieJar = cookieJar
#        self.networkAccessManager.setCookieJar(self.cookieJar)
        self.existFeeds = [] 
        self.doLike = self.config.get("doLike", 1) # 是否点赞
        self.doComment = self.config.get("doComment", 1) # 是否评论
        self.doTime = 10 # 此时间内的动态将进行操作
        self.interval = 1
        self.commentContentList = self.config.get("commentContentList", self.defaultCommentList)
#        self.moveToThread(self)
        self.doSignal.connect(self.getNewFeeds)
        self.restartSignal.connect(self.restart)
        #sys.exit()

    def saveConfig(self):

        self.__config.write()
    
    def setDoLike(self, flag):
        self.config["doLike"] = self.doLike = flag
        self.saveConfig()
     
    def setDoComment(self, flag):
        self.config["doComment"] = self.doComment = flag
        self.saveConfig()
    
    def setDoTime(self, value):
        self.doTime = value
        
    def setCommentContent(self, content):
        
        self.commentContentList = content.split("#")
        self.config["commentContentList"] = self.commentContentList
        self.saveConfig()
    
    def log(self, data, path="log.txt",method="a"):
        with open(path, method) as f:
            f.write(data.encode("u8") + " %s\n" % time.ctime())
    def stop(self):
        self.running = False
    def start_(self):
        self.workFinished = True
        self.running = True
    
    def run(self):
        while True:
            if self.running:
                if self.workFinished:
                    self.workFinished = False
#                    print "signal"
                    self.doSignal.emit()

            time.sleep(self.interval)

#        self.doSignal.emit()
    
            
    def httpGet(self, url):

        reply = self.networkAccessManager.get(QtNetwork.QNetworkRequest(QtCore.QUrl(url)))
        return reply

    def httpPost(self, url, param):
        
        param = urllib.urlencode(param)
        param = QtCore.QString(param).toUtf8()
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        request.setRawHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8")
        request.setRawHeader("Origin","http://user.qzone.qq.com")
        reply = self.networkAccessManager.post(request, param)
        return reply

    def getCallBackJson(self, data):
        """
        :data: QString
        """
        data = unicode(data, "utf-8")
        data = data[data.find("(") + 1: data.rfind(")")]
#        print data
#        data = "s = %s" % data
#        print data
        data = self.webFrame.evaluateJavaScript("JSON.stringify(%s)"%data).toString()
        data = json.loads(unicode(data))
        return data

    def tryDo(self, func):

        try:
            func()
        except Exception,e:
            self.log(traceback.format_exc(), self.errorLogPath)

    def getNewFeeds(self):

        self.tryDo(self._getNewFeeds)

    def _getNewFeeds(self):

        url = "http://user.qzone.qq.com/p/ic2.s8/cgi-bin/feeds/cgi_get_feeds_count.cgi?uin=%s&rd=0.0771736716851592&g_tk=%s" % (self.uin, self.gtk)
        self.newFeedsReply = self.httpGet(url)
        self.newFeedsReply.finished.connect(self.handleNewFeeds)
        #self.connect(self.newFeedsReply, QtCore.SIGNAL("finished()"), self.handleNewFeeds)

    def handleNewFeeds(self):

        self.tryDo(self._handleNewFeeds)

    def _handleNewFeeds(self):

        data = self.newFeedsReply.readAll()
        try:
            data = self.getCallBackJson(data)
            #print data
            self.log(unicode(data), method="w")
            if "login" in data["message"]:
                self.logSignal.emit(u"掉线了，需要重新登录！")
                self.stop()
                self.restartSignal.emit()
            elif data["data"]["newfeeds_uinlist"]:
                self.getFeeds()
        except:
            traceback.print_exc()
            self.workFinished = True
            return
        self.workFinished = True

    def getFeeds(self):

        self.tryDo(self._getFeeds)
    
    def _getFeeds(self):
        
        url = "http://user.qzone.qq.com/p/ic2.s8/cgi-bin/feeds/feeds3_html_more?\
uin=" + self.uin + "&scope=0&view=1&daylist=&uinlist=&gid=&flag=1&filter=all&applist=all&refresh=0&\
aisortEndTime=0&aisortOffset=0&getAisort=0&aisortBeginTime=0&pagenum=1&externparam=&firstGetGroup=0&\
icServerTime=0&mixnocache=0&scene=0&begintime=0&count=10&dayspac=0&sidomain=ctc.qzonestyle.gtimg.cn&useutf8=1&\
outputhtmlfeed=1&rd=0.04290125542320311&getob=1&g_tk=" + self.gtk
        self.feedsReply = self.httpGet(url)
        #self.log(url)
        self.connect(self.feedsReply , QtCore.SIGNAL("finished()"), self.handleFeeds)

    def handleFeeds(self):

        self.tryDo(self._handleFeeds)
        self.workFinished = True
    
    def _handleFeeds(self):
        
        data = self.feedsReply.readAll()
        #self.feedsReply.close()
#        self.feedsReply.deleteLater()
        #data = QtCore.QString(data)
        #data=unicode(data, "utf-8")
        #data = str(data)
        """
        try:
            print data,time.ctime()
        except:
            print repr(data),time.ctime()
#            self.log(data+"\n%s"%time.ctime())
        """
        #index = data.find("{")
        #self.log(unicode(data, "utf-8"),method="w")
        data = self.getCallBackJson(data)
        if not data:
            #print "not json"
            return
#        tmp = self.webFrame.evaluateJavaScript("console.log(%s)"%data)
        #tmp.deleteLater()
#        self.workFinished = True
#        print "slot"
#        return
        #data = unicode(data.toUtf8(), "utf-8")
        #self.logPlainTextEdit.setPlainText(data)
        #data = json.loads(data)
#        print data["message"]
        
        #data = eval(data)
        #self.log(str(data))
        for feed in data["data"]["data"]:
            if not feed:
                continue
            appid = feed["appid"]
            typeid = feed["typeid"]
            fid = feed["key"]
            abstime = feed["abstime"]
#            self.log(str(type(abstime)))
            authorUin = feed["uin"]
            nickName = feed["nickname"]
            strTime = feed["feedstime"]
            if (time.time() - int(abstime) )  > self.doTime or (authorUin + fid) in self.existFeeds:
                continue
            if self.doLike:
                self.likeFeed(appid, typeid, fid, authorUin, abstime)
                #break
                #time.sleep(1)
            if self.doComment and self.commentContentList:
                self.commentFeed(fid, authorUin, (random.choice(self.commentContentList)).encode("u8"), appid, abstime)

            self.existFeeds.append(authorUin + fid)
            self.logSignal.emit(u"%s(%s)有新动态，%s\n"%(nickName, authorUin, strTime))

#        self.logSignal.emit(u"一轮动态刷新完毕，%s\n"%time.ctime())
        """
        if self.running:
            self.doSignal.emit()
        """
        
    def likeFeed(self, appid, typeid, fid, authorUin, abstime):
        

        url = "http://w.qzone.qq.com/cgi-bin/likes/internal_dolike_app?g_tk=" + self.gtk
        if "311" == appid:
            #说说
            unikey = "http://user.qzone.qq.com/%s/mood/%s"%(authorUin, fid)
            curkey = unikey
        elif appid =="2":
            #原创日志
            unikey = "http://user.qzone.qq.com/%s/blog/%s"%(authorUin,abstime)
            curkey = unikey
        else:
            return
        param = {"qzreferrer":"http://user.qzone.qq.com/" + self.uin, "opuin":self.uin, "fid":fid, 
        "unikey":unikey, "curkey":curkey, "from":1, "appid":appid, "typeid":typeid, "abstime":abstime, "active":0, "fupdate":1}
        self.httpPost(url, param)
        
    def commentFeed(self, fid, authorUin,  content, appid,abstime):
        if "311" == appid:
            url = "http://user.qzone.qq.com/q/taotao/cgi-bin/emotion_cgi_re_feeds?g_tk=" + self.gtk
            topicId = "%s_%s__1"%(authorUin, fid)
        elif "202" == appid or "2" == appid:
            url = "http://b1.qzone.qq.com/cgi-bin/blognew/add_comment?g_tk=" + self.gtk
            topicId = "%s_%s"%(authorUin, abstime)
        else:
            return 
        param  = {"topicId": topicId, "feedsType":100, "inCharset":"utf-8", "outCharset":"utf-8", 
        "plat":"qzone", "source":"ic", "hostUin":authorUin, "uin":self.uin, "format":"fs", "ref":"feeds", "content":content, 
        "private":0, "paramstr":1,"qzreferrer":"http://user.qzone.qq.com/%s/infocenter"%self.uin, "isSignIn":"", "richval":"",  "richtype":""}
        self.postReply = self.httpPost(url, param)
        #self.logPlainTextEdit.appendPlainText(QtCore.QString(u"评论了啊"))
        #self.connect(self.postReply, QtCore.SIGNAL("finished()"), self.addReplyLog)


    def restart(self):

        arg = " %s" % self.uin
        cur_file = sys.argv[0]
        cmd = ("python __init__.py" + arg) if cur_file.endswith("pyc") or cur_file.endswith("py") else cur_file + arg
        print cmd
        #p = subprocess.Popen('runcmd %s' % cmd)
        p = subprocess.Popen(cmd)
        #os.system(cmd)
        #time.sleep(3)
        sys.exit()


#subprocess.Popen("python __init__.py autologin")
