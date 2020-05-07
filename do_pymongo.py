#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
mongodb 操作
提取集合(表)的字段名及字段类型
pip install pymongo
'''


from pymongo import MongoClient
import pandas as pd
 
client = MongoClient('mongodb://dds-bp186af14d7906841.mongodb.rds.aliyuncs.com:3717/')
#client = MongoClient('mongodb://username:password@dds-bp186af14d7906841.mongodb.rds.aliyuncs.com:3717/')
db = client.kzqixiu

db.authenticate("username", "password")
 
collection_list = db.list_collection_names()
print(collection_list)
#collection_list = db.po_order.find({})
coll = db.get_collection("so_order")

d = coll.find_one()
for i,j in d.items():
    print(i,type(j))

client.close()