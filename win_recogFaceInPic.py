# -*- coding: utf-8 -*-
#
from ui_win_recogFaceInPic import Ui_win_recogFaceInPic
import myLib
from PyQt5.QtWidgets import *

class Win_RecogFaceInPic(QWidget, Ui_win_recogFaceInPic):
    def __init__(self, parent=None ):
        super(Win_RecogFaceInPic, self).__init__(parent)
        self.setupUi(self)
        self.button_openPicFile.clicked.connect(self.open_pic_file)
    def open_pic_file(self):
        fname, _ = myLib.loadFile(self,'p')

