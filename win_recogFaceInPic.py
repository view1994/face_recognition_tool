# -*- coding: utf-8 -*-
#
from ui_win_recogFaceInPic import Ui_win_recogFaceInPic
import myLib,face_recog
from PyQt5.QtWidgets import *
import face_recognition
import cv2
from PyQt5.Qt import QImage,QPixmap
from PIL import Image,ImageDraw,ImageFont
class Win_RecogFaceInPic(QWidget, Ui_win_recogFaceInPic):
    def __init__(self, parent=None ):
        super(Win_RecogFaceInPic, self).__init__(parent)
        self.setupUi(self)
        self.button_openPicFile.clicked.connect(self.open_pic_file)
        self.commandLinkButton.clicked.connect(self.close)
    windowList = []
    ###### 重写关闭事件，回到第一界面
    def closeEvent(self, event):
        from mainWin import MainWindow
        mainWin = MainWindow()
        self.windowList.append(mainWin)  ##注：没有这句，是不打开另一个主界面的！
        mainWin.show()
        event.accept()
    def open_pic_file(self):
        fname, _ = myLib.loadFile(self,'p')
        self.textEdit.setText(fname)
        self.known_face_encodings, self.known_face_names = face_recog.get_featuresArray_fromDB()
        image = face_recognition.load_image_file(fname)
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # 默认为unknown
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
            face_names.append(name)
        # 将捕捉到的人脸显示出来
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #top *= 4
            #right *= 4
            #bottom *= 4
            #left *= 4
            # 矩形框
            cv2.rectangle(bgr_image, (left, top), (right, bottom), (0, 0, 255), 2)
            # 加上标签
            cv2.rectangle(bgr_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX

            #font = ImageFont.truetype('simhei.ttf', 50, encoding='utf-8')

            cv2.putText(bgr_image, name, (left + 6, bottom - 6), font, 2.0, (255, 255, 255), 1)
        img2 = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        Qimg = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        myLib.show_img_in_lable_center(self.label, QPixmap.fromImage(Qimg))
