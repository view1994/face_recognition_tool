# -*- coding: utf-8 -*-
#
import cv2
from PIL import Image
import face_recognition
import numpy
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from db import get_all_features

faces_info = []
face_num = 0
face_now = 0
known_face_encodings = []
known_face_names = []
def find_faces_locations_in(f_name):
    # 将jpg文件加载到numpy 数组中
    image = face_recognition.load_image_file(f_name)
    face_locations = face_recognition.face_locations(image)
    # 使用CNN模型, 另请参见: find_faces_in_picture_cnn.py
    # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
    return face_locations

def get_img_by_location(img,location):
    top, right, bottom, left = location
    #print(top, bottom, left, right,'raw')
    w = right - left
    h = bottom - top
    top = int(top - h / 5.0)
    top = top if top >= 0 else 0
    bottom = int(bottom + h / 5.0)
    bottom = bottom if bottom <= img.shape[0] else img.shape[0]
    right = int(right + w / 5.0)
    right = right if right <= img.shape[1] else img.shape[1]
    left = int(left - h / 5.0)
    left = left if left >= 0 else 0
    #print(top,bottom,left,right)
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
    return faces_info
#返回单张脸的list型特征数据
def get_face_encoding_of(face_image):
    encode_nparray = face_recognition.face_encodings(face_image)[0]
    encode_list = encode_nparray.tolist()
    return encode_list

def get_featuresArray_fromDB():
    features_li , names = get_all_features()
    features_array = []
    for i in features_li:
        features_array.append(numpy.array(i))
    return features_array,names

def update_knownFace_list():
    global known_face_encodings, known_face_names
    known_face_encodings, known_face_names = get_featuresArray_fromDB()

#视频和图片通用:
#video call: recog_in( bgrframe , update_features  = False ,frame_type = 'bgr_frame',scale_rate = 4.0 )
#pic call: recog_in( rgbframe , update_features  = True , frame_type = 'rgb_frame',scale_rate = 1.0 )
def recog_in( frame , update_features  = True ,frame_type = 'rgb',scale_rate = 1.0 ):
    from PIL import Image, ImageDraw, ImageFont
    #预处理
    if update_features :
        update_knownFace_list()
    if scale_rate != 1.0 :
        frame2 = cv2.resize(frame, (0, 0), fx = (1/scale_rate) , fy = ( 1/scale_rate ) )
    else:
        frame2 = frame
    if frame_type == "rgb":
        rgb_frame= frame
        rgb_frame_big = frame
        #bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  #cv画图用
    else:
        rgb_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        #bgr_frame = frame
        rgb_frame_big = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #编码
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        # 默认为unknown
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.39)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        face_names.append(name)
    # 将捕捉到的人脸标记出来
    pimg = Image.fromarray(rgb_frame_big.astype('uint8')).convert('RGB')
    print(type(pimg))
    draw = ImageDraw.Draw(pimg)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top = int(top * scale_rate)      #视频 scale_rate = 4
        right =int(right * scale_rate)
        bottom = int(bottom * scale_rate)
        left = int(left * scale_rate)

        w = right - left
        h = bottom - top
        top = int(top - h / 5.0)
        top = top if top >= 0 else 0
        bottom = int(bottom + h / 5.0)
        bottom = bottom if bottom <= frame.shape[0] else frame.shape[0]
        right = int(right + w / 5.0)
        right = right if right <= frame.shape[1] else frame.shape[1]
        left = int(left - h / 5.0)
        left = left if left >= 0 else 0
        # 第一个参数是字体文件的路径，第二个是字体大小cv2.GetSize(frame)

        # 第一个参数是文字的起始坐标，第二个需要输出的文字，第三个是字体颜色，第四个是字体类型
        #0,0,255  深蓝
        #0，255，255  蓝绿
        #255，0，0  红
        #0，255，0 绿
        #255，255，0  黄
        if name == "Unknown":
            fill = (255,0,0)
        else:
            fill = (0,255,255)
        line_width = int((bottom-top)/20)
        draw.line([(left, top), (left, bottom)], fill=fill,width=line_width)
        draw.line([(right, top), (right, bottom)], fill=fill,width=line_width)
        draw.line([(left, top), (right, top)], fill=fill,width=line_width)
        draw.line([(left, bottom), (right, bottom)], fill=fill,width=line_width)
        font_size = int((bottom - top - 12) // len(name))
        print(font_size)
        font = ImageFont.truetype('STHeiti Light.ttc', font_size, encoding='utf-8')
        draw.text((left + 6, bottom + 10), name, fill, font=font)
        #draw.rectangle((left,top),(0,255,255),outline=True)#blue

        # 矩形框
        #cv2.rectangle(bgr_frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # 加上标签
        #cv2.rectangle(bgr_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #font = cv2.FONT_HERSHEY_DUPLEX
        #'STHeiti Light.ttc'
        #cv2.putText(bgr_frame, name, (left + 6, bottom - 6), font, 2.0, (255, 255, 255), 1)
    #rgb_npImg = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
    #rgb_npImg = cv2.cvtColor(rgb_frame_big, cv2.COLOR_BGR2RGB)
    rgb_npImg = numpy.array(pimg)#np.array(rgb_frame_big)
    Qimg = QImage(rgb_npImg[:], rgb_npImg.shape[1], rgb_npImg.shape[0], rgb_npImg.shape[1] * 3, QImage.Format_RGB888)
    return Qimg

