#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Python编写FTP下载程序
'''
import ftplib  
import os  
import socket  
import sys  

HOST = 'ftp.ncdc.noaa.gov'  
#DIRN = r'/pub/data/gsod/1901'
#FILE = 'xue.jpg'  
USER_NAME = ''  
PWD = ''  
  
def DownloadFile(dir_name,file_name):  
    try:  
        f = ftplib.FTP(HOST)  
    except(socket.error, socket.gaierror) as e:  
        print('ERROR:cannot reach %s' % HOST)  
        return  
    print('*** Connected to host %s' % HOST)  
  
    try:  
        f.login(USER_NAME, PWD)  
    except ftplib.error_perm:  
        print('ERROR:cannot login USER_NAME=%s, PWD=%s' % (USER_NAME, PWD))  
        f.quit()  
        return  
    print('*** Logined in as %s' % USER_NAME)  
  
    try:  
        f.cwd(dir_name)  
    except ftplib.error_perm:  
        print('ERROR:cannot CD to %s' % dir_name)  
        f.quit()  
        return  
  
    try:  
        file = open(file_name, 'wb')  
        f.retrbinary('RETR %s' % file_name, file.write)  
        file.close()  
          
    except ftplib.error_perm:  
        print('ERROR:cannot read file %s' % file_name)  
        os.unlink(file_name)  
        file.close()  
    else:  
        print('*** Downloaded %s to %s' % (file_name, os.getcwd()))  
    f.quit()  
    return  
          
  
for i in range(1991,2000):
    dir_name = r'/pub/data/gsod/'+str(i)
    file_name = 'gsod_'+str(i)+'.tar'
    DownloadFile(dir_name,file_name)  