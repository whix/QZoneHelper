# -*- coding:UTF8 -*-

import threading
import json
import time
import urllib
import random
from PyQt4 import QtNetwork
from PyQt4 import QtWebKit
from PyQt4 import QtCore


class PythonJs(QtCore.QObject):

    jsonStr = QtCore.QString("")
    @QtCore.pyqtSignature("QString")
    def getJson(self,jsonStr):
        self.jsonStr = jsonStr

class Control(QtCore.QThread):
            
    doSignal = QtCore.pyqtSignal()
    logSignal = QtCore.pyqtSignal(str)
    def __init__(self, networkAccessManager, uin, gtk):
        super(Control, self).__init__()
        
        self.workFinished = True
        self.pythonJs = PythonJs()
        self.uin = uin
        self.gtk = gtk
        self.page = QtWebKit.QWebPage()
        self.webFrame = self.page.mainFrame()
        self.running = False
        self.networkAccessManager = networkAccessManager
        #self.networkAccessManager = QtNetwork.QNetworkAccessManager(self)
        #self.cookieJar = cookieJar
        #self.networkAccessManager.setCookieJar(self.cookieJar)
        self.existFeeds = []
        self.doLike = 1
        self.doComment = 1
        self.doTime = 10 # sec
        self.commentContentList = []
        self.webFrame.addToJavaScriptWindowObject("python", self.pythonJs)
#        self.moveToThread(self)
        self.doSignal.connect(self.getFeeds)
    
    def setDoLike(self, flag):
        self.doLike = flag
     
    def setDoComment(self, flag):
        self.doComment = flag
    
    def setDoTime(self, value):
        self.doTime = value
        
    def setCommentContent(self, content):
        
        self.commentContentList = content.split("#")
    
    def log(self, data):
        with open("log.txt", "w") as f:
            f.write(data.encode("u8"))
    def stop(self):
        self.running = False
    def start_(self):
        self.running = True
    
    def run(self):
        while True:
            if self.running:
                if self.workFinished:
                    self.wordFinished = False
                    self.doSignal.emit()

            time.sleep(1)

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
    
    def getFeeds(self):
        
        url = "http://user.qzone.qq.com/p/ic2.s8/cgi-bin/feeds/feeds3_html_more?\
uin=" + self.uin + "&scope=0&view=1&daylist=&uinlist=&gid=&flag=1&filter=all&applist=all&refresh=0&\
aisortEndTime=0&aisortOffset=0&getAisort=0&aisortBeginTime=0&pagenum=1&externparam=&firstGetGroup=0&\
icServerTime=0&mixnocache=0&scene=0&begintime=0&count=10&dayspac=0&sidomain=ctc.qzonestyle.gtimg.cn&useutf8=1&\
outputhtmlfeed=1&rd=0.04290125542320311&getob=1&g_tk=" + self.gtk
        self.feedsReply = self.httpGet(url)
        #self.log(url)
        self.connect(self.feedsReply , QtCore.SIGNAL("finished()"), self.handleFeeds)
    
    def handleFeeds(self):
        
        data = self.feedsReply.readAll()
        #data = QtCore.QString(data)
        #data=unicode(data, "utf-8")
        #data = str(data)
        data=unicode(data, "utf-8")
        try:
            print data,time.ctime()
        except:
            print repr(data),time.ctime()
#            self.log(data+"\n%s"%time.ctime())
        #index = data.find("{")
        data = data[len(u"_Callback("):-2]
        self.webFrame.evaluateJavaScript("python.getJson(JSON.stringify(%s))"%data)
        data = unicode(self.pythonJs.jsonStr.toUtf8(), "utf-8")
        if not data:
            print "not json"
            return
        #self.log(data)
        #self.logPlainTextEdit.setPlainText(data)
        data = json.loads(data)
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
            if not ((time.time() - int(abstime)) < self.doTime and ((authorUin+fid) not in self.existFeeds)):
                continue
            if self.doLike:
                self.likeFeed(appid, typeid, fid, authorUin, abstime)
                #break
                #time.sleep(1)
            if self.doComment and self.commentContentList:
                self.commentFeed(fid, authorUin, (random.choice(self.commentContentList)).encode("u8"), appid, abstime)
                self.logSignal.emit(u"%s(%s)有新动态，%s\n"%(nickName, authorUin, strTime))
                self.existFeeds.append(authorUin+fid)

#        self.logSignal.emit(u"一轮动态刷新完毕，%s\n"%time.ctime())
        self.workFinished = True
        """
        if self.running:
            self.doSignal.emit()
        """
        
    def likeFeed(self, appid, typeid, fid, authorUin, abstime):
        

        url = "http://w.qzone.qq.com/cgi-bin/likes/internal_dolike_app?g_tk=" + self.gtk
        if "311" == appid:
            #说说
            key = "http://user.qzone.qq.com/%s/mood/%s"%(authorUin, fid)
        elif "202" == appid or "2" == appid:
            #日志
            key = "http://user.qzone.qq.com/%s/blog/%s"%(authorUin,abstime)
        else:
            return
        param = {"qzreferrer":"http://user.qzone.qq.com/" + self.uin, "opuin":self.uin, "fid":fid, 
        "unikey":key, "curkey":key, "from":1, "appid":appid, "typeid":typeid, "abstime":abstime, "active":0, "fupdate":1}
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
