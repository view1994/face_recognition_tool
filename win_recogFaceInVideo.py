# -*- coding: utf-8 -*-
# 识别视频中人脸
from ui_win_recogFaceInVideo import Ui_win_recogFaceInVideo
import myLib, face_recog
from face_recog import *

class Win_RecogFaceInVideo(QWidget, Ui_win_recogFaceInVideo):
    def __init__(self, parent=None ):
        super(Win_RecogFaceInVideo, self).__init__(parent)
        self.setupUi(self)
        self.button_openCamera.setCheckable(True)
        self.button_openCamera.setAutoExclusive(True)
        self.button_openCamera.clicked.connect(self.recog_in_camera)
        self.button_openVideoFile.clicked.connect(self.open_video_file)
        self.commandLinkButton.clicked.connect(self.close)

    video_capture = []
    windowList = []
    ###### 重写关闭事件，回到第一界面
    def closeEvent(self, event):
        if self.button_openCamera.isChecked():
            self.recog_close()
        cv2.destroyAllWindows()
        from mainWin import MainWindow
        mainWin = MainWindow()
        self.windowList.append(mainWin)  ##注：没有这句，是不打开另一个主界面的！
        mainWin.show()
        event.accept()

    def open_video_file(self):
        self.button_openCamera.setEnabled(False)
        fname, ret = myLib.loadFile(self,'video')
        if ret :
            self.textEdit.setText(fname)
            self.recog_init( fname )

    def recog_in_camera(self):
        if  self.button_openCamera.isChecked():
            self.button_openVideoFile.setEnabled(False)
            self.button_openCamera.setText('关闭摄像头')
            self.recog_init(0)
        else:
            self.recog_close()

    def recog_init(self, fname = 0):
        face_recog.update_knownFace_list()
        self.video_capture = cv2.VideoCapture(fname)
        self.timer_camera = QTimer()
        self.timer_camera.start(10)
        self.timer_camera.timeout.connect(self.play1pic)  # 连接槽函数

    def recog_close(self):
        self.video_capture.release()
        self.timer_camera.stop()
        self.button_openCamera.setText('打开摄像头')
        self.button_openVideoFile.setEnabled(True)
        self.label.setText('请选择视频文件或打开摄像头')

    def play1pic(self):
        ret, frame = self.video_capture.read()
        if ret:
            Qimg = face_recog.recog_in(frame, update_features=False, frame_type='bgr', scale_rate=4.0)
            myLib.show_img_in_lable_center(self.label,QPixmap.fromImage(Qimg))
        else:
            self.video_capture.release()
            self.timer_camera.stop()
            self.button_openCamera.setEnabled(True)
