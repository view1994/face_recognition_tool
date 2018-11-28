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
    print('1--',features,type(features))
    s = set(features)
    features += [facial_feature]
    print('2--', features, type(features))
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


'''
def test():
    name = 'aa2'
    feature = [1,2,3,4]
    insert_data(name, feature)
    print(get_all_names())
    print(get_features_of(name))
    
    name = 'bb'
    feature = [3,7,6,5]
    insert_data(name, feature)
    print(get_features_of(name))
    print(get_all_names())
    delet_data_of(name)
    print(get_features_of(name))
    print(get_all_names())


#插入一条完整的信息，参数set为字典格式，包含'name','facial_feature'信息,'facial_feature'的值为列表
def insert_set(set):
    name = set['name']
    facial_feature = set['facial_feature']
    face_data.insert(set)


if __name__=="__main__":
    test()



face_data.update({"name":"zhangsan"},{'$set':{"age":20}})
for i in face_data.find():
    print(i)
for i in face_data.find({"name":"zhangsan"}):
    print(i)
'''