#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys,re
import codecs
    
"""
utf-8文件转为gbk文件
"""


def ReadFile(filePath,encoding="utf-8"):
    with codecs.open(filePath,"r",encoding) as f:
        return f.read()
 
def WriteFile(filePath,u,encoding="gbk"):
    with codecs.open(filePath,"w",encoding) as f:
        f.write(u)
 
def UTF8_2_GBK(src,dst):
    content = ReadFile(src,encoding="utf-8")
    WriteFile(dst,content,encoding="gbk")
    
    
UTF8_2_GBK('test.csv','t.csv')
