# -*- coding: utf-8 -*-
# !/usr/local/bin/python3.6
# file name: win_inputData.py
from PyQt5 import QtCore, QtGui, QtWidgets
'''
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
'''
from ui_win_inputData import Ui_win_inputData #ui_xx替换成ui文件的文件名
class Win_InputData(QtWidgets.QWidget, Ui_win_inputData):
    def __init__(self, parent=None):
        super(Win_InputData, self).__init__(parent)
        self.setupUi(self)
        #self.button_inputData.clicked.connect(self.button_inputData_clicked_Event)
        #self.button_recogFaceInPic.clicked.connect(self.button_recogFaceInPic_clicked_Event)
        #self.button_recogFaceInVideo.clicked.connect(self.button_recogFaceInVideo_clicked_Event)
    #添加若干个槽函数
    def button_inputData_clicked_Event(self):
        print('button_inputData clicked')
    def button_recogFaceInPic_clicked_Event(self):
        print('button_recogFaceInPic clicked')
    def button_recogFaceInVideo_clicked_Event(self):
        print('button_recogFaceInVideo clicked')
    def loadFile(self):
        print("load--file")
        # QFileDialog就是系统对话框的那个类,第一个参数是上下文，第二个参数是弹框的名字，第三个参数是开始打开的路径，第四个参数是需要的格式
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, '选择图片', '/Users/tanyashi/Pictures', 'Image files(*.jpg *.gif *.jpeg *.png)')
        self.show_img_in_lable_center(self.label, fname)
    def show_img_in_lable_center(self,lable,img_fname):
        pix_map = QtGui.QPixmap(img_fname)
        img_w = pix_map.width()
        img_h = pix_map.height()
        lab_w = lable.width()
        lab_h = lable.height()
        if (img_w > lab_w)|(img_h > lab_h):
            w_rate = float(img_w)/float(lab_w)
            h_rate = float(img_h)/float(lab_h)
            if w_rate >= h_rate :
                w = lab_w
                h = int(img_h/w_rate)
            else:
                w = int(img_w/h_rate)
                h = lab_h
        else:
            w = img_w
            h = img_h
        print('img_w={},img_h={},lab_w={},lab_h={},w={},h={}'.format(img_w, img_h, lab_w, lab_h, w, h))
        self.label.setPixmap(QtGui.QPixmap(img_fname).scaled(w,h))