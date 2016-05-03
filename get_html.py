#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,sys,requests
    
def getHtml(url):
    """
    伪装头部并得到网页内容
    """
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Host": "www.baidu.com",
    "X-Requested-With":"XMLHttpRequest"
    }


    session = requests.Session()
    session.headers = headers  
    html_bytes = session.get(url)
    print(type(html_bytes))
    print(html_bytes.encoding)  #查看网页编码
    html_bytes.encoding = 'ISO-8859-1'  #重新编码
    html_string = html_bytes.text
    return html_string    


def saveFile(data,filename):
    save_path = os.path.join(sys.path[0], filename)
    f_obj = open(save_path, 'w',encoding='utf-8') # w 表示打开方式
    #f_obj = open(save_path, 'w',encoding='cp1252') # 编码异常时尝试
    f_obj.write(data)
    f_obj.close()
    

# 爬取网页
url = 'https://www.baidu.com'    

html_doc = getHtml(url)  #返回一个网页文本文档
print(type(html_doc))
   
saveFile(html_doc,'baidu.html')

