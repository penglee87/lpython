#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Config(object):  
    DEBUG = False  
    TESTING = False  
    DATABASE_URI = 'sqlite://:memory:'  
  
class ProductionConfig(Config):  
    DATABASE_URI = 'mysql://user@localhost/foo'  
  
class DevelopmentConfig(Config):  
    DEBUG = True  
  
class TestingConfig(Config):  
    TESTING = True  
  
from flask import Flask  
app = Flask(__name__)  

#app.config.from_object('configmodule.ProductionConfig')  
#app.config.from_object(DevelopmentConfig)
app.config.from_object(ProductionConfig)

print (app.config.get('DEBUG')) 
print (app.config.get('DATABASE_URI'))