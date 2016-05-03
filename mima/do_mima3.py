#!/usr/bin/env python3
#coding=utf-8
"""
待修改
"""
import zipfile
import os
from threading import Thread
import time
#待解压文件的路径
path = r'testmima.zip'

def pojie_zip(path,password):
  if path[-4:]=='.zip':
    zip = zipfile.ZipFile(path, "r",zipfile.zlib.DEFLATED)
    #print zip.namelist()
    try:
      #若解压成功，则返回True,和密码
      zip.extractall(path=r'C:\Users\leadtone\Desktop\test\mima',members=zip.namelist() , pwd=password)
      print (' ----success!,The password is %s' % password)
      zip.close()
      return True
    except:
      pass  #如果发生异常，不报错
    #print 'error'
    
    
def get_pass():
  #密码字典的路径
  passPath=r'dict3.txt'
  passFile=open(passPath,'r')
  for line in passFile.readlines():
    password=line.strip('\n')
    #print 'Try the password %s' % password
    if pojie_zip(path,password):
      break
  passFile.close()
if __name__=='__main__':
  start=time.clock()
  get_pass()
  print ("done (%.2f seconds)" % (time.clock() - start))