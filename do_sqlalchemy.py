#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pymysql
pymysql.install_as_MySQLdb()
basedir = os.path.abspath(os.path.dirname(__file__))

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://root:root@127.0.0.1/test',echo=True)
Base = declarative_base()
class User(Base):
    __tablename__= 'users'
    id= Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)


Session = sessionmaker(bind=engine)
session = Session()

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)

print(session.query(User))
print(type(session.query(User)))
print(session.query(User.name,User.fullname))
#print(session.query(User).name)
#print(ed_user.query.all())

session.commit()
'''
for instance in session.query(User):
    print (instance.name,instance.password)
    

session.commit()
'''
