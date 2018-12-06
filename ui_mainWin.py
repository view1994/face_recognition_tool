# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainWin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_background = QtWidgets.QLabel(self.centralwidget)
        self.main_background.setGeometry(QtCore.QRect(0, 0, 450, 500))
        self.main_background.setText("")
        self.main_background.setPixmap(QtGui.QPixmap("../../../Pictures/IMG_0198.jpg"))
        self.main_background.setScaledContents(True)
        self.main_background.setObjectName("main_background")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(105, 95, 222, 296))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_inputData = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.button_inputData.setFont(font)
        self.button_inputData.setObjectName("button_inputData")
        self.verticalLayout.addWidget(self.button_inputData)
        self.button_recogFaceInPic = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.button_recogFaceInPic.setFont(font)
        self.button_recogFaceInPic.setObjectName("button_recogFaceInPic")
        self.verticalLayout.addWidget(self.button_recogFaceInPic)
        self.button_recogFaceInVideo = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.button_recogFaceInVideo.setFont(font)
        self.button_recogFaceInVideo.setObjectName("button_recogFaceInVideo")
        self.verticalLayout.addWidget(self.button_recogFaceInVideo)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_inputData.setText(_translate("MainWindow", "录入人脸数据"))
        self.button_recogFaceInPic.setText(_translate("MainWindow", "识别图中人脸"))
        self.button_recogFaceInVideo.setText(_translate("MainWindow", "识别视频画面中人脸"))

