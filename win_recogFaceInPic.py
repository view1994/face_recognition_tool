# -*- coding: utf-8 -*-
#
from ui_win_recogFaceInPic import Ui_win_recogFaceInPic
import myLib,face_recog
from PyQt5.QtWidgets import *
import face_recognition
from PyQt5.Qt import QPixmap
from PyQt5 import QtCore ,Qt
class Win_RecogFaceInPic(QWidget, Ui_win_recogFaceInPic):
    def __init__(self, parent=None ):
        super(Win_RecogFaceInPic, self).__init__(parent)
        self.setupUi(self)
        self.pix_map = None
        self.scrollArea.setGeometry(QtCore.QRect(20, 75, self.width() - 40, self.height() - 105))
        self.label.setGeometry(QtCore.QRect(0, 0, self.scrollArea.width(), self.scrollArea.height()))
        self.button_openPicFile.clicked.connect(self.open_pic_file)
        self.commandLinkButton.clicked.connect(self.close)
        self.button_recogFaceInPic.clicked.connect(self.recog_start)
        self.button_recogFaceInPic.setEnabled(False)
        self.button_picBigSize.clicked.connect(self.change_pic_size)
    windowList = []
    ###### 重写关闭事件，回到第一界面
    def closeEvent(self, event):
        from mainWin import MainWindow
        mainWin = MainWindow()
        self.windowList.append(mainWin)  ##注：没有这句，是不打开另一个主界面的！
        mainWin.show()
        event.accept()
    def open_pic_file(self):
        fname, ret = myLib.loadFile(self,'p')
        if ret:
            self.textEdit.setText(fname)
            self.button_recogFaceInPic.setEnabled(True)
            pix_map = QPixmap(fname)
            self.pix_map = pix_map
            myLib.show_img_in_lable_center(self.label, pix_map)


    def recog_start(self):
        fname = self.textEdit.toPlainText()
        image = face_recognition.load_image_file(fname)
        Qimg = face_recog.recog_in(image, update_features=True, frame_type='rgb', scale_rate=1.0)
        self.pix_map = QPixmap.fromImage(Qimg)
        myLib.show_img_in_lable_center(self.label, self.pix_map)
    def change_pic_size(self):
        if not self.button_picBigSize.isChecked():
            self.scrollArea.setGeometry(QtCore.QRect(20, 75, self.width() - 40, self.height() - 105))
            self.label.setText('请选择照片')
            if self.pix_map:
                self.label.setGeometry(QtCore.QRect(0,0, self.pix_map.width(), self.pix_map.height()))
                self.label.setPixmap(self.pix_map)
            self.button_picBigSize.setText('适应窗口显示')
        else:
            self.scrollArea.setGeometry(QtCore.QRect(20, 75, self.width() - 40, self.height() - 105))
            self.button_picBigSize.setText('原始大小显示')
            self.label.setText('请选择照片')
            self.label.setGeometry(QtCore.QRect(0, 0, self.scrollArea.width(),self.scrollArea.height()))
            if self.pix_map:
                myLib.show_img_in_lable_center(self.label, self.pix_map)
