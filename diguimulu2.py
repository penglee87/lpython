#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
递归目录,替换文件字符串
''' 
import os  
#递归遍历目录,将文件全路径存为列表(不含目录)
def dirlist(path, allfile):  
    filelist =  os.listdir(path)  
  
    for filename in filelist:  
        filepath = os.path.join(path, filename)  
        if os.path.isdir(filepath):  
            dirlist(filepath, allfile)  
        else:  
            allfile.append(filepath)  
    return allfile  
  
  
def find_str(filename):
    #打开文件
    with open(filename,'r+', encoding='utf-8', errors='ignore') as fh:
        #按文件查找
        file_content = fh.read()
        if 'qccr' in file_content:
            new_content=file_content.replace('qccr','gmail')
            fh.seek(0, 0)
            fh.write(new_content)
            print(filename)
            
        #按行查找
        '''
        lines = fh.readlines()
        for line in lines:
            if 'qccr' in line:
                print(filename)
        '''

allfile=dirlist(r'C:\Users\Administrator\Desktop\test\lpython', [])
for f in allfile:
    fh = find_str(f)
