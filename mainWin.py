# -*- coding: utf-8 -*-
# !/usr/local/bin/python3.6
# file name: mainWin.py
from PyQt5 import QtCore, QtGui, QtWidgets
'''
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
'''
from myLib import *
from ui_mainWin import Ui_MainWindow #ui_xx替换成ui文件的文件名
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.button_inputData.clicked.connect(self.button_inputData_clicked_Event)
        self.button_recogFaceInPic.clicked.connect(self.button_recogFaceInPic_clicked_Event)
        self.button_recogFaceInVideo.clicked.connect(self.button_recogFaceInVideo_clicked_Event)
    #添加若干个槽函数
    def button_inputData_clicked_Event(self):
        from win_inputData import Win_InputData
        #import sys
        print('button_inputData clicked')
        #app = QtWidgets.QApplication(sys.argv)
        winInputData = Win_InputData()
        #self.hide()
        winInputData.show()
        print("show input data window")
        #sys.exit(app.exec_())

    def button_recogFaceInPic_clicked_Event(self):
        print('button_recogFaceInPic clicked')
    def button_recogFaceInVideo_clicked_Event(self):
        print('button_recogFaceInVideo clicked')
    def loadFile(self):
        print("load--file")
        # QFileDialog就是系统对话框的那个类,第一个参数是上下文，第二个参数是弹框的名字，第三个参数是开始打开的路径，第四个参数是需要的格式
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, '选择图片', '/Users/tanyashi/Pictures', 'Image files(*.jpg *.gif *.jpeg *.png)')
        pix_map = QtGui.QPixmap(fname)
        show_img_in_lable_center(self.label, pix_map)
