#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import urllib.request
import urllib
 
from collections import deque

import http.cookiejar

#爬取百度主页
# head: dict of header
def makeMyOpener(head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

oper = makeMyOpener()
uop = oper.open('http://www.baidu.com/', timeout = 1000)
#urllib.request.install_opener(oper)  
#也可用上述方法将浏览器安装为默认，然后直接用 urllib.request.urlopen(url) 调用现在模拟的浏览器

data = uop.read()
data = data.decode('UTF-8')
#print(data.decode())

def saveFile(data):
    save_path = r'C:\Users\Administrator\Documents\GitHub\lspider\spider03.txt'
    f_obj = open(save_path, 'w',encoding='utf-8') # w 表示打开方式
    f_obj.write(data)
    f_obj.close()

saveFile(data)