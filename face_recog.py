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
        img2 = cv2.resize(src=np_img, dsize=None, fx=0.2, fy=0.2)
        face['Qimg'] = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        faces_info.append(face)
        #print('\n========face[img]======\n',face['img'])
    return faces_info

def get_face_encoding_of(face_image):
    return face_recognition.face_encodings(face_image)

def main():
    pass


if __name__ == '__main__':
    main()

