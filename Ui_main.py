# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sun Feb 01 01:41:18 2015
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(951, 675)
        Form.setMaximumSize(QtCore.QSize(951, 675))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/QZone.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(_fromUtf8(""))
        self.webView = QtWebKit.QWebView(Form)
        self.webView.setGeometry(QtCore.QRect(20, 10, 911, 651))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.frame = QtGui.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 951, 681))
        self.frame.setMaximumSize(QtCore.QSize(951, 681))
        self.frame.setStyleSheet(_fromUtf8("background-image: url(:/img/16.jpg);"))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.startPushButton = QtGui.QPushButton(self.frame)
        self.startPushButton.setGeometry(QtCore.QRect(190, 350, 75, 23))
        self.startPushButton.setStyleSheet(_fromUtf8(""))
        self.startPushButton.setObjectName(_fromUtf8("startPushButton"))
        self.stopPushButton = QtGui.QPushButton(self.frame)
        self.stopPushButton.setGeometry(QtCore.QRect(640, 350, 75, 23))
        self.stopPushButton.setStyleSheet(_fromUtf8(""))
        self.stopPushButton.setObjectName(_fromUtf8("stopPushButton"))
        self.logPlainTextEdit = QtGui.QPlainTextEdit(self.frame)
        self.logPlainTextEdit.setGeometry(QtCore.QRect(180, 440, 541, 151))
        self.logPlainTextEdit.setStyleSheet(_fromUtf8("background-image: url(:/img/logBackground.png);"))
        self.logPlainTextEdit.setReadOnly(True)
        self.logPlainTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.logPlainTextEdit.setBackgroundVisible(False)
        self.logPlainTextEdit.setObjectName(_fromUtf8("logPlainTextEdit"))
        self.doLikeCheckBox = QtGui.QCheckBox(self.frame)
        self.doLikeCheckBox.setGeometry(QtCore.QRect(490, 70, 61, 21))
        self.doLikeCheckBox.setStyleSheet(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/赞.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.doLikeCheckBox.setIcon(icon1)
        self.doLikeCheckBox.setChecked(True)
        self.doLikeCheckBox.setObjectName(_fromUtf8("doLikeCheckBox"))
        self.doCommentCheckBox = QtGui.QCheckBox(self.frame)
        self.doCommentCheckBox.setGeometry(QtCore.QRect(570, 70, 71, 21))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/评论.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.doCommentCheckBox.setIcon(icon2)
        self.doCommentCheckBox.setChecked(True)
        self.doCommentCheckBox.setObjectName(_fromUtf8("doCommentCheckBox"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(259, 70, 21, 20))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet(_fromUtf8("background-image: url(:/img/透明.jpg);"))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(350, 70, 141, 21))
        self.label_2.setStyleSheet(_fromUtf8("background-image: url(:/img/透明.jpg);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.timeSpinBox = QtGui.QSpinBox(self.frame)
        self.timeSpinBox.setGeometry(QtCore.QRect(290, 70, 51, 22))
        self.timeSpinBox.setStyleSheet(_fromUtf8("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));"))
        self.timeSpinBox.setWrapping(False)
        self.timeSpinBox.setObjectName(_fromUtf8("timeSpinBox"))
        self.commentContentPlainTextEdit = QtGui.QPlainTextEdit(self.frame)
        self.commentContentPlainTextEdit.setGeometry(QtCore.QRect(185, 150, 531, 191))
        self.commentContentPlainTextEdit.setStyleSheet(_fromUtf8("background-image: url(:/img/16.jpg);"))
        self.commentContentPlainTextEdit.setPlainText(_fromUtf8("秒赞是一种技术，你不需要怀疑！#专注秒赞百余年，值得信赖！#秒赞不是病，不赞却要命"))
        self.commentContentPlainTextEdit.setBackgroundVisible(False)
        self.commentContentPlainTextEdit.setObjectName(_fromUtf8("commentContentPlainTextEdit"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(230, 110, 441, 31))
        self.label_3.setStyleSheet(_fromUtf8("background-image: url(:/img/透明.jpg);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(410, 400, 61, 31))
        self.label_4.setStyleSheet(_fromUtf8("background-image: url(:/img/透明.jpg);"))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.feedBackPushButton = QtGui.QPushButton(self.frame)
        self.feedBackPushButton.setGeometry(QtCore.QRect(844, 640, 81, 23))
        self.feedBackPushButton.setObjectName(_fromUtf8("feedBackPushButton"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "QZoneHelper V1.0", None))
        self.startPushButton.setText(_translate("Form", "开始", None))
        self.stopPushButton.setText(_translate("Form", "停止", None))
        self.doLikeCheckBox.setText(_translate("Form", "秒赞", None))
        self.doCommentCheckBox.setText(_translate("Form", "秒评", None))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">对</span></p></body></html>", None))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">秒以内的动态进行</span></p></body></html>", None))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">下方输入评论语，多条以#隔开，评论时随机抽取其中一条</span></p></body></html>", None))
        self.label_4.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">动态们</span></p></body></html>", None))
        self.feedBackPushButton.setText(_translate("Form", "给作者提意见", None))

from PyQt4 import QtWebKit
import main_rc
