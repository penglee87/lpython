#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os,sys
import urllib.request, urllib.parse, http.cookiejar
import requests
import re
from datetime import datetime

def getcontent(url): 
    text_string = requests.get(url).text
    #正则匹配出轮胎列表
    html_string = re.findall(r'<a class=\\"item-name\\"(.*?)href=\\"//(.*?)target=\\"_blank\\">(.*?)</a>(.*?)class=\\"c-price\\">(.*?)                            </span>(.*?)class=\\"sale-num\\">(.*?)</span>(.*?)<span>评价:(.*?)</span>(.*?)',text_string)
    tuhupage = []

    # 循环遍历轮胎列表
    for tuhu in html_string:
        wangzhi = tuhu[1]
        mingcheng = tuhu[2]
        price = tuhu[4]
        xiaoliang = tuhu[6]
        pingjia = tuhu[8]
        tuhupage.append((wangzhi,mingcheng,price,xiaoliang,pingjia))
    # 返回轮胎列表
    return tuhupage

def gethercontent(page):
    tuhulist = []
    #https://tuhucn.tmall.com/i/asynSearch.htm?_ksTS=1453466239320_1206&callback=jsonp1207&mid=w-11681573747-0&wid=11681573747&path=/category-753373497.htm&&spm=a1z10.5-b.w4011-11681573747.392.yLWQRY&catName=%C6%B7%C5%C6%C2%D6%CC%A5&catId=753373497&search=y&pageNo=3&scid=753373497
    url = 'https://tuhucn.tmall.com/i/asynSearch.htm?_ksTS=1453466239320_1206&callback=jsonp1207&mid=w-11681573747-0&wid=11681573747&path=/category-753373497.htm&&spm=a1z10.5-b.w4011-11681573747.392.yLWQRY&catName=%C6%B7%C5%C6%C2%D6%CC%A5&catId=753373497&search=y&pageNo='     # 基础网址

    for i in range(1,page):           
        urll = url+str(i)+'&scid=753373497'
        print(urll)
        content = getcontent(urll)
        tuhulist.append(content)
    return tuhulist

def saveFile(tuhulist):
    '''
    将列表保存为文件
    '''
    save_path = os.path.join(sys.path[0], "tuhu_tianmao"+datetime.now().strftime('%Y%m%d')+".csv")    
    f_obj = open(save_path, 'w',encoding='utf-8')
    title = ['网址','轮胎名称','价格', '销量','评价人数']
    html = '\t'.join(title)+ '\n'
    for page in tuhulist:
        for luntai in page:
            html += '\t'.join(luntai) + '\n'
    f_obj.write(html)
    f_obj.close()

page = 15   # 总共爬到多少页
html_doc = gethercontent(page)
saveFile(html_doc)
# 生成的csv默认为ASCII编码，用记事本打开另存为ASCII编码，然后打开再转Excel等
