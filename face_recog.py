# -*- coding: utf-8 -*-
#
import cv2
from PIL import Image
import face_recognition
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

faces_info = []
face_num = 0
face_now = 0
def find_faces_locations_in(f_name):
    # 将jpg文件加载到numpy 数组中
    image = face_recognition.load_image_file(f_name)
    face_locations = face_recognition.face_locations(image)
    # 使用CNN模型, 另请参见: find_faces_in_picture_cnn.py
    # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
    return face_locations

def get_img_by_location(img,location):
    top, right, bottom, left = location
    return img[top:bottom, left:right]

def find_faces_in(f_name):
    image = face_recognition.load_image_file(f_name)
    face_locations = face_recognition.face_locations(image)
    global face_num,face_now,faces_info
    faces_info = []
    face_num = len(face_locations)
    face_now = 0
    for face_location in face_locations:
        face = {}
        np_img = get_img_by_location(image,face_location)
        face['location'] = face_location
        face['np_img'] = np_img
        img2 = cv2.resize(src=np_img, dsize=None, fx=1, fy=1)
        face['Qimg'] = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        faces_info.append(face)
        #print('\n========face[img]======\n',face['img'])
    return faces_info
#返回单张脸的list型特征数据
def get_face_encoding_of(face_image):
    encode_nparray = face_recognition.face_encodings(face_image)[0]
    encode_list = encode_nparray.tolist()
    return encode_list
def get_encoding_array_from(li):
    import numpy
    return numpy.array(li)
def get_featuresArray_fromDB():
    from db import get_all_features
    features_li , names = get_all_features()
    features_ar = []
    for i in features_li:
        features_ar.append(get_encoding_array_from(i))
    return features_ar,names
def find_name_of(np_img):
    pass
def main():
    pass


if __name__ == '__main__':
    main()

