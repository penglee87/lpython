#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

f1 = open(r'test_ANSI.txt','r')  #wineows下解析ansi的文件
content1 = f1.read()
print(content1)
f1.close()


f2 = codecs.open(r'test_utf8.txt', 'w',encoding='utf8',errors='strict')   #wineows下解析uft8无bom的文件,utf8仍存在问题
content2 = f2.read()
print(content2)
f2.close()


"""
>>> import sys
>>> sys.stdout.encoding
'cp936'
>>> s='aaa'
>>> type(s)
<class 'str'>
>>> import sys
>>> s.encode(encoding='UTF-8')
b'aaa'
>>> s.encode(encoding='UTF-8').decode()
'aaa'
"""


"""
# windows下编码问题修复
import sys  
  
class UnicodeStreamFilter:  
    def __init__(self, target):  
        self.target = target  
        self.encoding = 'utf-8'  
        self.errors = 'replace'  
        self.encode_to = self.target.encoding  
    def write(self, s):  
        if type(s) == str:
            s = s.decode("utf-8")  
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)  
        self.target.write(s)  


print(sys.stdout.encoding)       
if sys.stdout.encoding == 'cp936':
    #print('type(sys.stdout)',type(sys.stdout))
    sys.stdout = UnicodeStreamFilter(sys.stdout)


if __name__ == "__main__":
    print(sys.stdout.encoding)
    a = "你好"  
    b = u"你好"  
    print (a)  
    print (b)  
    
"""