#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class A:   
    def __init__(self):   
        self.name = 'zhangjing'  
        self.age = 24
    def method(self):   
        print("method print")
  
Instance = A()

print (getattr(Instance , 'name', 'not find'))  #如果Instance 对象中有属性name则打印self.name的值,否则打印'not find'
print (getattr(Instance , 'age', 'not find'))   #如果Instance 对象中有属性age则打印self.age的值,否则打印'not find'
print (getattr(Instance , 'agee', 'not find'))  #如果Instance 对象中有属性age则打印self.age的值,否则打印'not find'

print (getattr(Instance, 'method', 'default'))    #如果有方法method,则打印其地址,否则打印default 
print (getattr(Instance, 'method', 'default')())  #如果有方法method,运行函数并打印None,否则打印default