# -*- coding: utf-8 -*-
# 摄像头头像识别
import face_recognition
import cv2
from ui_win_recogFaceInVideo import Ui_win_recogFaceInVideo
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer
import sys
import myLib, face_recog ,cv2

from face_recog import *



class Win_RecogFaceInVideo(QWidget, Ui_win_recogFaceInVideo):
    def __init__(self, parent=None ):
        super(Win_RecogFaceInVideo, self).__init__(parent)
        self.setupUi(self)
        self.button_openCamera.setCheckable(True)
        self.button_openCamera.setAutoExclusive(True)
        self.button_openCamera.clicked.connect(self.recog_in_camera)
        self.button_openVideoFile.clicked.connect(self.open_video_file)
        self.commandLinkButton.clicked.connect(self.back2main)
        #self.button_openCamera.triggered.connect(self.close_camera())
    windowList = []
    ###### 重写关闭事件，回到第一界面
    def closeEvent(self, event):
        from mainWin import MainWindow
        mainWin = MainWindow()
        self.windowList.append(mainWin)  ##注：没有这句，是不打开另一个主界面的！
        mainWin.show()
        event.accept()
    def back2main(self):
        print('video_capture.release')
        if self.button_openCamera.isChecked():
            self.close_camera()
        cv2.destroyAllWindows()
        self.close()

    video_capture = []
    def open_video_file(self):
        self.button_openCamera.setEnabled(False)
        fname, _ = myLib.loadFile(self,'video')
        self.textEdit.setText(fname)
        self.video_capture = cv2.VideoCapture(fname)
        self.known_face_encodings, self.known_face_names = face_recog.get_featuresArray_fromDB()
        self.timer_camera = QTimer()
        self.timer_camera.start(10)  # 1000ms == 1s
        self.timer_camera.timeout.connect(self.play1pic)  # 连接槽函数

    def recog_in_camera(self):
        if  self.button_openCamera.isChecked():
            self.button_openVideoFile.setEnabled(False)
            self.button_openCamera.setText('关闭摄像头')
            self.video_capture = cv2.VideoCapture(0)
            self.known_face_encodings, self.known_face_names = face_recog.get_featuresArray_fromDB()
            self.timer_camera = QTimer()
            self.timer_camera.start(10)  # 1000ms == 1s
            self.timer_camera.timeout.connect(self.play1pic)  # 连接槽函数
        else:
            self.close_camera()
    def close_camera(self):
        self.video_capture.release()
        self.timer_camera.stop()
        self.button_openCamera.setText('打开摄像头')
        self.button_openVideoFile.setEnabled(True)
        self.label.setText('请选择视频文件或打开摄像头')
        #self.label.setPixmap(None)
    def play1pic(self):
        ret, frame = self.video_capture.read()
        if ret:
            bgr_frame = self.recog_in_v(frame)
            img2 = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
            Qimg = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
            myLib.show_img_in_lable_center(self.label,QPixmap.fromImage(Qimg))
            #self.label.setPixmap(QPixmap.fromImage(Qimg))
        else:
            self.video_capture.release()
            self.timer_camera.stop()
            self.button_openCamera.setEnabled(True)
    def recog_in_v(self,bgr_frame):
        # 改变摄像头图像的大小，图像小，所做的计算就少
        small_frame = cv2.resize(bgr_frame, (0, 0), fx=0.25, fy=0.25)
        #BGR->RGB
        rgb_small_frame = small_frame[:,:,::-1]
        # 根据encoding来判断是不是同一个人，是就输出true，不是为flase
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
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
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # 矩形框
            cv2.rectangle(bgr_frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # 加上标签
            cv2.rectangle(bgr_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(bgr_frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        return bgr_frame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    winRecogInVideo1 = Win_RecogFaceInVideo()
    winRecogInVideo1.show()
    print("show input data window")
    sys.exit(app.exec_())