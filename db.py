#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

conn = MongoClient('localhost', 27017)#创建本地连接，localhost指本地连接
db = conn.face_recog  #连接face_recog数据库，没有则自动创建
face_data = db.facial_features #使用test_set集合，没有则自动创建

#获取名字为name的脸部特征数据，返回值为list
def get_features_of(name):
    data = [i for i in face_data.find({"name":name})]
    #print(data,(True if data else False))
    if data:
        return data[0]['facial_feature']
    else:
        return []
#插入一张人脸信息，facial_feature为一条特征信息
def insert_data(name,facial_feature):
    features = get_features_of(name)
    features += [facial_feature]
    face_data.update({"name": name}, {'$set': {"facial_feature": features}},upsert=True)
#获取所有人物名称
def get_all_names():
    names = []
    for i in face_data.find():
        names.append(i['name'])
    return names
#删除某人的人脸信息
def delet_data_of(name):
    face_data.remove({'name': name})
#获取数据库中全部人物及数据量，供显示数据库信息使用
def get_all_namesAndNum():
    name_nums = []
    for i in face_data.find():
        name_nums.append([i['name'],len(i['facial_feature'])])
    return name_nums
#获取全部面部特征向量列表及与之对应的人物列表,供人脸匹配使用
def get_all_features():
    features = []
    names = []
    for i in face_data.find():
        features += i['facial_feature']
        names += [i['name']] * len(i['facial_feature'])
    return features,names


def test():
    import face_recognition
    name = 'view'
    VIEW_PIC_NAME = "/Users/tanyashi/Pictures/441542133958_.pic.jpg"
    # 将jpg文件加载到numpy数组中
    view_image = face_recognition.load_image_file(VIEW_PIC_NAME)
    view_face_encoding = face_recognition.face_encodings(view_image)[0]
    print(view_face_encoding)
    feature = list(view_face_encoding)
    insert_data(name, feature)
    print(get_all_names())
    print(get_features_of(name))
    print(get_all_features())
    delet_data_of('view')


#插入一条完整的信息，参数set为字典格式，包含'name','facial_feature'信息,'facial_feature'的值为列表
def insert_set(set):
    name = set['name']
    facial_feature = set['facial_feature']
    face_data.insert(set)

'''
if __name__=="__main__":
    test()


face_data.update({"name":"zhangsan"},{'$set':{"age":20}})
for i in face_data.find():
    print(i)
for i in face_data.find({"name":"zhangsan"}):
    print(i)
'''