# -*- coding: utf-8 -*-
#
from PyQt5 import QtCore, QtGui, QtWidgets

#加载图像文件，第一个返回值是文件名
#def loadPicFile(self):
    #print("load--file")
    # QFileDialog就是系统对话框的那个类,第一个参数是上下文，第二个参数是弹框的名字，第三个参数是开始打开的路径，第四个参数是需要的格式
#    return QtWidgets.QFileDialog.getOpenFileName( self , '加载图片', '/Users/tanyashi/Pictures',
#                                                 'Image files(*.jpg *.gif *.jpeg *.png)')


#加载文件，第一个返回值是文件名
def loadFile(self , fileType):
    if fileType in ['p','P','photo','pic','*.jpg',' *.gif ','*.jpeg',' *.png']:
        type =  'Image files(*.jpg *.gif *.jpeg *.png)'
        title = '加载图片'
        path = '/Users/tanyashi/Pictures'
    elif fileType in ['v','V','video','mp4','*.mp4',' *.avi','*.mkv',' *.mov']:
        type = 'Video files(*.mp4 *.avi *.mkv *.mov)'
        title = '加载视频'
        path = '/Users/tanyashi/Movies'
    return  QtWidgets.QFileDialog.getOpenFileName( self , title, path ,type)


#在指定标签中居中显示指定图像文件
def show_img_in_lable_center( label, pix_map):
    img_w = pix_map.width()
    img_h = pix_map.height()
    lab_w = label.width()
    lab_h = label.height()
    if (img_w > lab_w) | (img_h > lab_h):
        w_rate = float(img_w) / float(lab_w)
        h_rate = float(img_h) / float(lab_h)
        if w_rate >= h_rate:
            w = lab_w
            h = int(img_h / w_rate)
        else:
            w = int(img_w / h_rate)
            h = lab_h
    else:
        w = img_w
        h = img_h
    #print('img_w={},img_h={},lab_w={},lab_h={},w={},h={}'.format(img_w, img_h, lab_w, lab_h, w, h))
    label.setPixmap(pix_map.scaled(w, h))




if __name__ == '__main__':
    pass
'''

'''