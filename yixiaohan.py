#!/usr/bin/env python3
'''
查找子目录中文件最多的一个目录
'''
import os
folder=r'C:\Users\Administrator\Desktop\yixiaohan'
filelist=[]

childfile=os.listdir(folder)
# and os.path.isdir(childfile)==1
filelist=[(folder+os.path.sep+f) for f in childfile]
for i in filelist:
    if os.path.isdir(i):
        print (i,len(os.listdir(i)))
