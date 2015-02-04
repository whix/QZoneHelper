#coding=UTF8
import re
import json
import time
import threading
import os
import traceback
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtNetwork
from Ui_main import Ui_Form
from control import Control
from dataconfig import Config

CONFIG_PATH = "config"

class Recorder(QtCore.QObject):


    def setConfig(self, config):
        self.config = config

    @QtCore.pyqtSignature("QString, QString")
    def getQQPwd(self, u, p):
        data = self.config.get(str(u))
        #print "qq",u
        self.qq = str(u)
        data["pwd"] = str(p)
        self.config.write()
        #print u,p

class Main(QtGui.QWidget, Ui_Form):

    loadFinishedSignal = QtCore.pyqtSignal()
    def __init__(self):

        self.baseJs = """
        var ce = document.createEvent('MouseEvent'); 
        ce.initEvent('click', false, false); 
        login_btn = document.getElementById("login_button");
        u = document.getElementById("u");
        p = document.getElementById("p");
        sw = document.getElementById("switcher_plogin");
        setTimeout(function(){sw.dispatchEvent(ce);}, 1000);
        var oldClick = login_btn.click;
        function getQQPwd()
        {
            python.getQQPwd(u.value, p.value);
            login_btn.onclick = oldClick;
            login_btn.dispatchEvent(ce);
            login_btn.onclick = getQQPwd;
            //alert("login");
        }
        login_btn.onclick = getQQPwd;

        """
        self.version = 1.1
        self.lyc = "http://0yuchen.com"
        super(Main, self).__init__()
        self.setupUi(self)
        self.setSoftNameTitile()
        self.page = self.webView.page()
        self.webFrame = self.page.currentFrame()
        self.nam = self.page.networkAccessManager()
        self.cookieJar = self.nam.cookieJar()
        self.url = "http://qzone.qq.com"
        self.gtk = ""
        self.skey = ""
        self.uin = ""
        self.qq = sys.argv[1] if len(sys.argv) > 1 else None
        self.pwd = ""
        #self.start_cmd = "autologin"
        self.isAutoLogin = True if self.qq else False
        self.logined = False
        self.loadFinishedSignal.connect(self.loginFrameFinished)
        self.__config = Config()
        #print self.__config
        self.connect(self.nam, QtCore.SIGNAL("finished(QNetworkReply *)"), self.getInfo)
        self.connect(self.startPushButton, QtCore.SIGNAL("clicked()"), self.startClicked)
        self.connect(self.stopPushButton, QtCore.SIGNAL("clicked()"), self.stopClicked)
        self.feedBackPushButton.clicked.connect(self.feedBack)
        self.webView.loadFinished.connect(self.loadFinished)
        #self.connect(self.postPushButton, QtCore.SIGNAL("clicked()"), self.postClicked)
        self.webFrame.load(QtCore.QUrl(self.url))
        self.pythonjs = Recorder()
        self.pythonjs.setConfig(self.__config)
        self.show()
        #self.thread = QtCore.QThread()
        #self.startPushButton.hide()
        #self.logPlainTextEdit.hide()
        self.frame.hide()
        self.timeSpinBox.setValue(10)
        self.checkUpdate()

    def setSoftNameTitile(self):
        
        self.setWindowTitle(QtCore.QString(u"QZoneHelper V%.1f" % self.version))

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
        
        self.qq = self.pythonjs.qq
        self.__config["lastQQ"] = self.qq
        self.__config.write()
        self.webView.hide()
        #self.startPushButton.show()
        #self.logPlainTextEdit.show()
        self.frame.show()
        #self.resize(946, 461)
        self.control = Control(self.nam, self.uin, self.gtk, self.__config)
        #self.control.moveToThread(self.thread)
        #self.control.uin = self.uin
        #self.control.gtk = self.gtk
#        self.control.doSignal.connect(self.control.getFeeds)
        self.control.logSignal.connect(self.addLog)
        #self.thread.started.connect(lambda:self.control.work( self.cookieJar, self.uin, self.gtk))
        #self.thread.start()
        self.timeSpinBox.valueChanged.connect(self.control.setDoTime)
        self.doLikeCheckBox.stateChanged.connect(self.control.setDoLike)
        #print self.qq
        config = self.__config.get(self.qq)
        if not config.get("doLike", 1):
            self.doLikeCheckBox.setChecked(False)
        self.doCommentCheckBox.stateChanged.connect(self.control.setDoComment)
        if not config.get("doComment", 1):
            self.doCommentCheckBox.setChecked(False)
        self.commentContentPlainTextEdit.textChanged.connect(self.setCommentContent)
        commentTextList = config.get("commentContentList", self.control.defaultCommentList)
        commentText = "#".join(commentTextList)
        self.commentContentPlainTextEdit.setPlainText(QtCore.QString(commentText))
        self.setCommentContent()
        self.control.start()
        if self.isAutoLogin:
            self.startClicked()

        self.setSoftNameTitile()

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
        self.addLog(u"动态刷新开始...一旦有新动态将会进行操作，您可以最小化软件忙别的了~\n")
#        self.control.start()

    def stopClicked(self):
        self.control.stop()
        self.addLog(u"软件已停止！\n")
#        self.control.start()

    def loginFrameFinished(self):

        #print "jhio"
        #print self.webFrame.url()
        #print self.webFrame.baseUrl()
        #print self.webFrame.frameName()
        #time.sleep(2)
        if self.isAutoLogin:
            self.autoLogin()
        else:
            self.setDefaultQQPwd()
        #print self.webFrame.frameName()
        #print "finished"

    def loadFinished(self):

        #print self.webFrame.url().toString()
        if self.logined:
            return True
        #time.sleep(1)
        #print self.webFrame.url()
        self.webFrame = self.webFrame.childFrames()[0]
        self.webFrame.addToJavaScriptWindowObject("python", self.pythonjs)
        self.webFrame.evaluateJavaScript(self.baseJs)
        #self.webFrame.loadFinished.connect(self.loginFrameFinished)
        #self.webFrame.initialLayoutCompleted.connect(self.loginFrameFinished)
        self.logined = True
        self.loadFinishedSignal.emit()
        self.setWindowTitle(QtCore.QString(u"登录中...."))

    def makeJs(self, js):

        js = "try{setTimeout(function(){%s}, 1000)}catch(e){alert(e)}" % js

        return js
    
    def setDefaultQQPwd(self):

        lastQQ = self.__config.get("lastQQ")
        if not lastQQ:
            return
        #print lastQQ
        lastPwd = self.__config.get(lastQQ)
        lastPwd = None if not lastPwd else lastPwd.get("pwd", None)
        js = """
        u.value = "%s";
        p.value = "%s";
        //alert(u.value);
        """ % (lastQQ, lastPwd)
        js = self.makeJs(js)
        self.webFrame.evaluateJavaScript(js)

    def autoLogin(self):

        #print self.__config
        js =  """
        u.value = "%s";
        p.value = "%s";
        function login_()
        {
            
            login_btn.dispatchEvent(ce);
            alert("我登!");
            //login_btn.click()
        }
        //login_();
        getQQPwd();
        setTimeout(getQQPwd, 1000);
        //login_btn.dispatchEvent(ce);
        //login_btn.dispatchEvent(ce);
        //alert("a");
        """ % (self.qq, self.__config.get(self.qq)["pwd"])
        #print js
        js = self.makeJs(js)
        self.webFrame.evaluateJavaScript(js)

    def getInfo(self, reply):

        #print reply.url().toString()
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

class QApp(QtGui.QApplication):

    def __init__(self,argv):
        super(QApp,self).__init__(argv)

    def notify(self,obj,event):

        f = open("error.txt","a")
        try:
            return super(QApp,self).notify(obj,event)
        except:
            traceback.print_exc(file=f)


app = QApp(sys.argv)
main = Main()
sys.exit(app.exec_())
