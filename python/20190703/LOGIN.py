# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LOGIN.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!


from aip import AipSpeech
from aip import AipNlp

from PyQt5 import QtCore, QtGui, QtWidgets
import tts
import sys



class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(930, 804)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 690, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 690, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(514, 690, 101, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(720, 690, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(110, 50, 741, 241))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(110, 350, 741, 271))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 10, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 310, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 930, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.tts)
        self.pushButton_2.clicked.connect(MainWindow.nlg)
        self.pushButton_3.clicked.connect(MainWindow.nlu)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "语音合成"))
        self.pushButton_2.setText(_translate("MainWindow", "摘要生成"))
        self.pushButton_3.setText(_translate("MainWindow", "自然语言理解"))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "输入"))
        self.label_2.setText(_translate("MainWindow", "输出内容(路径)"))



    def tts(self):
        APP_ID = '16707980'
        API_KEY = 'v9iWBNX8usLfy2MuDWQGSX2Q'
        SECRET_KEY = 'xBOEUHxuFh6SmwCEjmag147fzsGgTVfF'

        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        contents=self.textEdit.toPlainText()

        result = client.synthesis(contents, 'zh', 1, {
            'vol': 5,
        })

        import os
        self.textEdit_2.setPlainText(os.path.join(sys.path[0],"result.wav"))
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open(os.path.join(sys.path[0],"result.wav"), 'wb') as f:
                f.write(result)


    def nlg(self):
        APP_ID = '16707980'
        API_KEY = 'v9iWBNX8usLfy2MuDWQGSX2Q'
        SECRET_KEY = 'xBOEUHxuFh6SmwCEjmag147fzsGgTVfF'

        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

        contents=self.textEdit.toPlainText()

        maxSummaryLen = 100

        """ 调用新闻摘要接口 """
        client.newsSummary(contents, maxSummaryLen);

        """ 如果有可选参数 """
        options = {}
        options["title"] = "标题"

        """ 带参数调用新闻摘要接口 """
        result = client.newsSummary(contents, maxSummaryLen, options)
        self.textEdit_2.setPlainText(result['summary'])
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码

        print("yes")

    def nlu(self):
        APP_ID = '16707980'
        API_KEY = 'v9iWBNX8usLfy2MuDWQGSX2Q'
        SECRET_KEY = 'xBOEUHxuFh6SmwCEjmag147fzsGgTVfF'
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

        contents = self.textEdit.toPlainText()


        # print(result)


        self.textEdit_2.setPlainText("**********情感分析**********");
        # 情感分析
        result = client.sentimentClassify(contents)  # 情感分析
        self.textEdit_2.append(str(result['items']))

        self.textEdit_2.append("**********情感极性类别（积极、消极、中性）的判断**********")
        options = {}
        options["type"] = 13
        result = client.commentTag(contents, options)
        self.textEdit_2.append(str(result['items']))

        #对文章按照内容类型进行自动分类，首批支持娱乐、体育、科技等26个主流内容类型
        self.textEdit_2.append("**********对文章按照内容类型进行自动分类，首批支持娱乐、体育、科技等26个主流内容类型**********")
        title = "1"
        result = client.topic(title, contents)  # 对文章按照内容类型进行自动分类，首批支持娱乐、体育、科技等26个主流内容类型
        self.textEdit_2.append(str(result['item']))






if __name__=="__main__":
    import sys
    from PyQt5.QtGui import QIcon
    app=QtWidgets.QApplication(sys.argv)
    # widget=QtWidgets.QWidget()
    ui=Ui_MainWindow()
    # ui.setupUi(widget)
    # widget.setWindowIcon(QIcon('web.png'))#增加icon图标，如果没有图片可以没有这句
    ui.show()
    sys.exit(app.exec_())