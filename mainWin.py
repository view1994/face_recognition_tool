# -*- coding: utf-8 -*-
# !/usr/local/bin/python3.6
# file name: mainWin.py
from myLib import *
from ui_mainWin import Ui_MainWindow #ui_xx替换成ui文件的文件名
from win_inputData import Win_InputData
from win_recogFaceInVideo import Win_RecogFaceInVideo
from win_recogFaceInPic import Win_RecogFaceInPic

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.button_inputData.clicked.connect(self.button_inputData_clicked_Event)
        self.button_recogFaceInPic.clicked.connect(self.button_recogFaceInPic_clicked_Event)
        self.button_recogFaceInVideo.clicked.connect(self.button_recogFaceInVideo_clicked_Event)
    #添加若干个槽函数
    windowList = []
    def button_inputData_clicked_Event(self):
        winInputData = Win_InputData()
        self.windowList.append(winInputData)
        self.close()
        winInputData.show()
    def button_recogFaceInPic_clicked_Event(self):
        winRecogeFaceInVideo = Win_RecogFaceInPic()
        self.windowList.append(winRecogeFaceInVideo)
        self.close()
        winRecogeFaceInVideo.show()
    def button_recogFaceInVideo_clicked_Event(self):
        winRecogeFaceInVideo = Win_RecogFaceInVideo()
        self.windowList.append(winRecogeFaceInVideo)
        self.close()
        winRecogeFaceInVideo.show()
    def loadFile(self):
        # QFileDialog就是系统对话框的那个类,第一个参数是上下文，第二个参数是弹框的名字，第三个参数是开始打开的路径，第四个参数是需要的格式
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, '选择图片', '/Users/tanyashi/Pictures', 'Image files(*.jpg *.gif *.jpeg *.png)')
        pix_map = QtGui.QPixmap(fname)
        show_img_in_lable_center(self.label, pix_map)
