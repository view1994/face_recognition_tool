# -*- coding: utf-8 -*-
# 摄像头头像识别
import face_recognition
import cv2
from ui_win_recogFaceInVideo import Ui_win_recogFaceInVideo
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import myLib, face_recog ,cv2
import db
from face_recog import *
from PIL import Image


class Win_RecogFaceInVideo(QWidget, Ui_win_recogFaceInVideo):
    def __init__(self, parent=None ):
        super(Win_RecogFaceInVideo, self).__init__(parent)
        self.setupUi(self)
        self.button_openCamera.clicked.connect(self.recog_in_camera)




    def recog_in_camera(self):
        video_capture = cv2.VideoCapture(0)
        # Create arrays of known face encodings and their names
        # 脸部特征数据的集合 # 人物名称的集合
        known_face_encodings , known_face_names = face_recog.get_featuresArray_fromDB()
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        while True:
            # 读取摄像头画面
            ret, frame = video_capture.read()
            # 改变摄像头图像的大小，图像小，所做的计算就少
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
            rgb_small_frame = small_frame[:, :, ::-1]
            # Only process every other frame of video to save time
            if process_this_frame:
                # 根据encoding来判断是不是同一个人，是就输出true，不是为flase
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # 默认为unknown
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]
                    face_names.append(name)
            process_this_frame = not process_this_frame
            # 将捕捉到的人脸显示出来
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # 矩形框
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                #加上标签
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # Display
            cv2.imshow('monitor', frame)
            # 按Q退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    winRecogInVideo1 = Win_RecogFaceInVideo()
    winRecogInVideo1.show()
    print("show input data window")
    sys.exit(app.exec_())