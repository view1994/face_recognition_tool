# -*- coding: utf-8 -*-
# !/usr/local/bin/python3.6
# file name: win_inputData.py
import myLib, face_recog
import db
from face_recog import *
from ui_win_inputData import Ui_win_inputData #ui_xx替换成ui文件的文件名
cache_data = []
cache_name_list = []
db_name_list = db.get_all_names()
db_name_num_list = db.get_all_namesAndNum()

class Win_InputData(QWidget, Ui_win_inputData):
    def __init__(self, parent=None):
        super(Win_InputData, self).__init__(parent)
        self.setupUi(self)
        nameList = ['choose name']
        nameList += db_name_list
        nameList.append('add new name')
        print(nameList)
        self.comboBox_chooseName.addItems(nameList)
        self.button_choosePic.clicked.connect(self.choosePic)
        self.button_lastFace.setEnabled(False)
        self.button_nextFace.setEnabled(False)
        self.button_lastFace.clicked.connect(self.clickedLastFace)
        self.button_nextFace.clicked.connect(self.clickedNextFace)
        self.edit_picPath.textChanged.connect(self.loadPicFileUsePath)
        self.button_nameConfirm.clicked.connect(self.addNameToCache)
        self.comboBox_chooseName.currentTextChanged.connect(self.addNewName)
        self.model = QStandardItemModel()
        self.model.setColumnCount(2)
        self.model.setHeaderData(0,Qt.Horizontal,'name')
        self.model.setHeaderData(1,Qt.Horizontal,"info_nums")
        for i in range(len(db_name_num_list)):
            #print('name:',db_name_num_list[i][0],'\tnum=',db_name_num_list[i][1])
            self.model.setItem(i,0,QStandardItem(db_name_num_list[i][0]))
            self.model.setItem(i,1,QStandardItem(str(db_name_num_list[i][1])))
        self.table_nameInDB.setModel(self.model)
        self.table_nameInDB.setColumnWidth(self.table_nameInDB.width()/2,self.table_nameInDB.width()/2)
        self.model2 = QStandardItemModel()
        self.model2.setColumnCount(2)
        self.model2.setHeaderData(0, Qt.Horizontal, 'name')
        self.model2.setHeaderData(1, Qt.Horizontal, "face")
        self.table_confirmedNames.setModel(self.model2)
        self.button_addData2DB.clicked.connect(self.addCache2DB)
        self.button_clearCache.clicked.connect(self.clearCache)
        self.button_back2main.clicked.connect(self.close)
    # 添加若干个槽函数
    windowList = []
    ###### 重写关闭事件，回到第一界面
    def closeEvent(self, event):
        from mainWin import MainWindow
        mainWin = MainWindow()
        self.windowList.append(mainWin)  ##注：没有这句，是不打开另一个主界面的！
        mainWin.show()
        event.accept()
    def clearCache(self):
        global cache_data
        cache_data = []
        self.checkCacheInfo()
    def addCache2DB(self):
        global cache_data
        while cache_data:
            data = cache_data.pop()
            db.insert_data( data['name'], data['facial_feature'])
        self.checkCacheInfo()
        self.checkDBInfo()
    def checkDBInfo(self):
        global db_name_list,db_name_num_list
        db_name_list = db.get_all_names()
        db_name_num_list = db.get_all_namesAndNum()
        for i in range(len(db_name_num_list)):
            #print('name:',db_name_num_list[i][0],'\tnum=',db_name_num_list[i][1])
            self.model.setItem(i,0,QStandardItem(db_name_num_list[i][0]))
            self.model.setItem(i,1,QStandardItem(str(db_name_num_list[i][1])))
    def checkCacheInfo(self):
        #print('cache_data:',cache_data)
        self.model2.clear()
        self.model2.setColumnCount(2)
        self.model2.setHeaderData(0, Qt.Horizontal, 'name')
        self.model2.setHeaderData(1, Qt.Horizontal, "face")
        for i in range(len(cache_data)):
            self.model2.setItem(i, 1, QStandardItem('第{}张'.format(cache_data[i]['index_now'])))
            self.model2.setItem(i, 0, QStandardItem(cache_data[i]['name']))
        self.table_confirmedNames.setModel(self.model2)
    def addNewName(self):
        name = self.comboBox_chooseName.currentText()
        if name == 'add new name':
            new_name, ok = QInputDialog.getText(self, "add new name", "请输入新名字\n注意：不要与已有名字相同！", QLineEdit.Normal, "")
            name_list = set(cache_name_list + db_name_list)
            if ok & (new_name not in name_list):
                #cache_data.append(new_data)
                cache_name_list.append(new_name)
                self.comboBox_chooseName.insertItem(1, new_name)
                self.comboBox_chooseName.setCurrentText(new_name)
            else:
                self.comboBox_chooseName.setCurrentIndex(0)
    def addNameToCache(self):
        name = self.comboBox_chooseName.currentText()
        if name == 'choose name':
            pass
        elif name == 'add new name':
            self.addNewName()
        else:
            np_img = face_recog.faces_info[face_recog.face_now]['np_img']
            new_encode = get_face_encoding_of(np_img)
            new_data = {}
            new_data['name'] = name
            new_data['facial_feature'] = new_encode
            new_data['index_now'] = face_recog.face_now+1
            cache_data.append(new_data)
            cache_name_list.append(name)
            self.checkCacheInfo()
    def choosePic(self):
        fname, ret = myLib.loadFile(self,'p')
        if ret :
            self.loadPicFile(fname)
            self.check_buttonStatus()
            self.edit_picPath.setText(fname)
    def loadPicFile(self,fname):
        print(fname)
        pix_map = QPixmap(fname)
        myLib.show_img_in_lable_center(self.label_rawPic, pix_map)
        face_recog.find_faces_in(fname)
        from face_recog import faces_info
        if len(faces_info):
            self.label_recogNote.setText('已识别出{}张人脸，请为他们录入名字：\n第{}张：'.format(len(faces_info),face_recog.face_now+1))
            self.label_faceImg.setPixmap(QPixmap.fromImage(faces_info[0]['Qimg']))
            return True
        else:
            self.label_recogNote.setText('该图像中未识别出人脸,请重新选择照片。')
            self.label_faceImg.setText('识别失败')
            return False
    def loadPicFileUsePath(self):
        fname = self.edit_picPath.toPlainText()
        if '\n' in fname:
            fname = fname.replace('\n','')
            self.loadPicFile(fname)
            self.check_buttonStatus()
            self.edit_picPath.setText(fname)
    def check_buttonStatus(self):
        from face_recog import face_now, face_num,faces_info
        self.label_recogNote.setText('已识别出{}张人脸，请为他们录入名字：\n第{}张：'.format(len(faces_info), face_now + 1))
        if face_recog.face_now == 0:
            self.button_lastFace.setText('没有\n上一张')
            self.button_lastFace.setDisabled(True)
        else:
            self.button_lastFace.setEnabled(True)
            self.button_lastFace.setText('上一张')
        if face_now == (face_num-1):
            self.button_nextFace.setText('没有\n下一张')
            self.button_nextFace.setEnabled(False)
        else:
            self.button_nextFace.setEnabled(True)
            self.button_nextFace.setText('下一张')
    def clickedLastFace(self):
        if face_recog.face_now > 0:
            face_recog.face_now -=1
            self.label_faceImg.setPixmap(QPixmap.fromImage(face_recog.faces_info[face_recog.face_now]['Qimg']))
        self.check_buttonStatus()
    def clickedNextFace(self):
        from face_recog import face_now, face_num, faces_info
        if face_recog.face_now < face_num:
            face_recog.face_now = face_now + 1
            self.label_faceImg.setPixmap(QPixmap.fromImage(faces_info[face_recog.face_now]['Qimg']))
        self.check_buttonStatus()
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    winInputData = Win_InputData()
    winInputData.show()
    print("show input data window")
    sys.exit(app.exec_())
'''