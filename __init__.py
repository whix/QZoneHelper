#coding=UTF8
import re
import json
import time
import threading
import os
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtNetwork
from Ui_main import Ui_Form
from control import Control

class Test(QtGui.QWidget, Ui_Form):

    def __init__(self):
        self.version = 1.0
        self.lyc = "http://0yuchen.com"
        super(Test, self).__init__()
        self.setupUi(self)
        self.page = self.webView.page()
        self.webFrame = self.page.currentFrame()
        self.nam = self.page.networkAccessManager()
        self.cookieJar = self.nam.cookieJar()
        self.url = "http://qzone.qq.com"
        self.gtk = ""
        self.skey = ""
        self.uin = ""
        self.connect(self.nam, QtCore.SIGNAL("finished(QNetworkReply *)"), self.getInfo)
        self.connect(self.startPushButton, QtCore.SIGNAL("clicked()"), self.startClicked)
        self.connect(self.stopPushButton, QtCore.SIGNAL("clicked()"), self.stopClicked)
        self.feedBackPushButton.clicked.connect(self.feedBack)
        #self.connect(self.postPushButton, QtCore.SIGNAL("clicked()"), self.postClicked)
        self.webFrame.load(QtCore.QUrl(self.url))
        self.show()
        #self.thread = QtCore.QThread()
        #self.startPushButton.hide()
        #self.logPlainTextEdit.hide()
        self.frame.hide()
        self.timeSpinBox.setValue(10)
        self.checkUpdate()
        

    def feedBack(self):
        os.system("start %s"%(self.lyc))

    def checkUpdate(self):
        url = "http://update.0yuchen.com/qzonehelper.php"
        self.checkUpdateReply = self.nam.get(QtNetwork.QNetworkRequest(QtCore.QUrl(url)))
        self.checkUpdateReply.finished.connect(self.update)
    
    def update(self):
        try:
            self._update()
        except:
            pass
    
    def _update(self):
        result = self.checkUpdateReply.readAll()
        data=unicode(result, "utf-8")
        data = eval(data)
        print data
        if data["ver"] > self.version:
            if not QtGui.QMessageBox.question(None,QtCore.QString(u"发现新版本"),\
            QtCore.QString(u"是否更新?"),QtCore.QString("Yes!"),QtCore.QString("No!")):                
                #self.webFrame.load(QtCore.QUrl("http://0yuchen.com"))
                os.system("start %s"%data["url"])

    def readyOk(self):
        
        self.webView.hide()
        #self.startPushButton.show()
        #self.logPlainTextEdit.show()
        self.frame.show()
        #self.resize(946, 461)
        self.control = Control(self.nam, self.uin, self.gtk)
        #self.control.moveToThread(self.thread)
        #self.control.uin = self.uin
        #self.control.gtk = self.gtk
#        self.control.doSignal.connect(self.control.getFeeds)
        self.control.logSignal.connect(self.addLog)
        #self.thread.started.connect(lambda:self.control.work( self.cookieJar, self.uin, self.gtk))
        #self.thread.start()
        self.timeSpinBox.valueChanged.connect(self.control.setDoTime)
        self.doLikeCheckBox.stateChanged.connect(self.control.setDoLike)
        self.doCommentCheckBox.stateChanged.connect(self.control.setDoComment)
        self.commentContentPlainTextEdit.textChanged.connect(self.setCommentContent)
        self.setCommentContent()
        self.control.start()

    def setCommentContent(self):
        text = self.commentContentPlainTextEdit.toPlainText()
        text = unicode(text.toUtf8(), "utf8")
        self.control.setCommentContent(text)

    def get_gtk(self,skey):

        hash = 5381
        for i in range(len(skey)):
            hash += (hash << 5) + ord(skey[i])
        result = hash & 2147483647
        return str(result)

        #self.logPlainTextEdit.setPlainText(data)
    def startClicked(self):
        self.control.start_()
        self.addLog(u"动态刷新开始...\n")
#        self.control.start()

    def stopClicked(self):
        self.control.stop()
        self.addLog(u"软件已停止！\n")
#        self.control.start()

    def getInfo(self, reply):

        header = reply.request().rawHeader("X-Real-Url")
        header = str(header)

        if header == "":
            return
        uin = re.findall("uin=(\d+)", header)
        if uin:
            self.uin = uin[0]
        manager = reply.manager()
        for cookie in manager.cookieJar().allCookies():
            if str(cookie.name()) == "skey":
                skey = cookie.value()
                self.skey = unicode(skey)
        if not self.skey or self.gtk:
            return
        self.gtk = self.get_gtk(self.skey)
        self.readyOk()


    def addLog(self, content):
        self.logPlainTextEdit.appendPlainText(QtCore.QString(content))

import sys
app = QtGui.QApplication(sys.argv)
test = Test()
sys.exit(app.exec_())
