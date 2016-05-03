#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 实现修改文本文件中的内容
"""
import os
Const_File_Format=["sql","txt"]
def WriteXXLog(logfile_read,logfile_apend):
    file_object_read = open(logfile_read, 'r') 
    try:
        stringsave=""
        stringread=file_object_read.readline()
        while stringread:
            stringread=stringread.replace('CREATE', 'Alter')
            stringsave=stringsave+stringread
            stringread=file_object_read.readline()
        file_object_save = open(logfile_apend, 'w')
        file_object_save.write(stringsave)
        #file_object_save.name=file_object_read.name+'_alter'
    finally:
        file_object_read.close()
        file_object_save.close()
        
def GetFileFormat(fileName):
    if fileName:
        BaseName=os.path.basename(fileName)
        str=BaseName.split(".")
        return str[-1]
    else:
        return fileName

def DirSeekFile(dir):
    global Const_File_Format
    fileList=list()
    for s in os.listdir(dir):
        newDir=dir+"/"+s
        if os.path.isdir(newDir):
            self.DirSeekFile(newDir)
        else:
            if os.path.isfile(newDir):
                if newDir and (GetFileFormat(newDir) in Const_File_Format):
                    fileList.append(newDir)
    return fileList

def test_main():
    fileList=DirSeekFile('d:\\files')
    for k in  fileList:
        WriteXXLog(k,k)
if __name__ == "__main__":
    test_main()

