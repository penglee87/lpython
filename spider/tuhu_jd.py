#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os,sys,re
import requests
import json
import datetime

def tuhu_jd(url_content):
    
    soup = BeautifulSoup(url_content, 'html.parser') # 开始解析 
    tuhutable = soup.find_all('li', class_='jSubObject')  # 找到所有轮胎所在标记

    # 循环遍历轮胎列表
    for tuhu in tuhutable:
        subsoup = BeautifulSoup(str(tuhu), 'html.parser')
        wangzhi = subsoup.find('div', class_="jDesc").a['href']
        xinghao = subsoup.find('div', class_="jDesc").a.string
        price_id = subsoup.find('span',class_='jdNum')['jdprice']
        #price_id = re.search(r'<span jdprice=\"(.*?)\" jshop',str(tuhu)).group(1)
        price_json = requests.get(price_url + str(price_id)).json()
        price = str(price_json[0]['p'])

        tuhus.append((wangzhi,xinghao,price))
    # 返回轮胎列表
    return tuhus
    
    
def saveFile(data,filename):
    save_path = os.path.join(sys.path[0], filename)
    f_obj = open(save_path, 'w',encoding='utf-8') # w 表示打开方式
    f_obj.write(str(data))
    f_obj.close()
    
def list2file(tuhuslist):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    save_path = os.path.join(sys.path[0], "tuhujd"+yesterday.strftime('%Y%m%d')+".csv")
    f_obj = open(save_path, 'w',encoding='utf-8') # w 表示打开方式
    title = ['网址','轮胎名称', '价格']
    html = '\t'.join(title)+ '\n'
    for luntai in tuhuslist:
        html += '\t'.join(luntai) + '\n'
    f_obj.write(html)
    f_obj.close()
    
    
tuhus = []    
urllist = []  # 要爬取的网页
price_url=r'http://p.3.cn/prices/mgets?skuids=J_'
url1 = 'http://module-jshop.jd.com/module/getModuleHtml.html?appId=438176&orderBy=5&direction=1&categoryId=0&pageSize=24&venderId=138830&isGlobalSearch=0&maxPrice=0&pagePrototypeId=17&pageNo='
url2 = '&shopId=134686&minPrice=0&pageInstanceId=22214036&moduleInstanceId=22214043&prototypeId=68&templateId=401682&layoutInstanceId=22214043&origin=0&callback=jshop_module_render_callback&_=1461853465663'     # 基础网址
page = 25                                        # 总共爬到多少页

for i in range(1,page):           
    urll = url1+str(i)+url2
    print(urll)
    html_doc = requests.get(urll).text
    s = re.search(r'jshop_module_render_callback\((.*)\)',html_doc).group(1)
    d = json.loads(s)
    url_content = d['moduleText']
    tuhus = tuhu_jd(url_content)
list2file(tuhus)
#saveFile(url_content,'text.html')
#saveFile(html_doc,'tuhu_jd.txt')