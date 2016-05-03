#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import os,sys
from bs4 import BeautifulSoup
from datetime import datetime
import time

def tuhu(url_content):
    """
    输入网页内容进行轮胎爬取
    返回轮胎信息元组
    """
    tuhus = []
    soup = BeautifulSoup(url_content, 'html.parser') # 开始解析 

    # tuhutable = soup.select('div.indent table div a')
    tuhutable1 = soup.find_all("tr")  # 找到所有轮胎所在标记

    # 循环遍历轮胎列表
    for tuhu in tuhutable1:
        simpletuhu = tuhu
        # print(simpletuhu)

        subsoup = BeautifulSoup(str(simpletuhu), 'html.parser')
        wangzhi = subsoup.find('td',attrs={"class": "td1"}).a['href']
        xinghao = subsoup.find('td',attrs={"class": "td1"}).img['title']
        #xiaoliang = subsoup.find('td',attrs={"class": "td3"}).em.string
        #price = subsoup.find('td',attrs={"class": "td3"}).strong.string
        
        if  subsoup.find('td',attrs={"class": "td3"}).em is None:
            xiaoliang = '0'
        else:
            xiaoliang = subsoup.find('td',attrs={"class": "td3"}).em.string
          
        if  subsoup.find('td',attrs={"class": "td3"}).strong is None:
            price = '0'
        else:
            price = subsoup.find('td',attrs={"class": "td3"}).strong.string

        tuhus.append((wangzhi,xinghao, xiaoliang,price))
    # 返回轮胎列表
    return tuhus

    
def list2file(tuhuslist):
    '''
    保存文件
    '''
    save_path = os.path.join(sys.path[0], "tuhuguanwang"+datetime.now().strftime('%Y%m%d')+".csv")
    f_obj = open(save_path, 'w',encoding='utf-8') # w 表示打开方式
    title = ['网址','轮胎名称', '购买人数','价格']
    html = '\t'.join(title)+ '\n'
    for page in tuhuslist:
        for luntai in page:
            html += '\t'.join(luntai) + '\n'
    f_obj.write(html)
    f_obj.close()

    
@asyncio.coroutine
def fetch_page(session, url):
    with aiohttp.Timeout(10):
        response =  yield from session.get(url)
        assert response.status == 200
        try:
            content = yield from response.text()
        finally:
            yield from response.release()
        tuhus = tuhu(content)
        tuhu_list.append(tuhus)
        return tuhu_list
        
t1=time.time()
tuhu_list = []       
urllist = ['http://item.tuhu.cn/List/Tires.html']  # 要爬取的网页
url = 'http://item.tuhu.cn/List/Tires/'     # 基础网址
page = 13                                         # 总共爬到多少页

for i in range(2,page):
    urllist.append(url+str(i)+'.html')
try:
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop) 
    #tasks = [fetch_page(session, 'http://item.tuhu.cn/List/Tires.html'),fetch_page(session, 'http://item.tuhu.cn/List/Tires/2.html')]
    tasks = [fetch_page(session, url) for url in urllist]
    content = loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    list2file(tuhu_list)
finally:
    session.close()
    t2=time.time()
    
print(t2-t1)
    