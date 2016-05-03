#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys
import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup
    
@asyncio.coroutine    
def tuhu(url):
    """
    输入网页内容进行轮胎爬取
    返回轮胎信息元组
    """
    response = yield from session.get(url, allow_redirects=False)
    try:
        if response.status == 200:        
            url_content = yield from response.text()
            
            soup = BeautifulSoup(url_content, 'html.parser') # 开始解析 
            
            tuhutable = soup.find_all("tr")  # 找到所有轮胎所在标记
            
            # 循环遍历轮胎列表
            for tuhu in tuhutable:        
                subsoup = BeautifulSoup(str(tuhu), 'html.parser')
                wangzhi = subsoup.find('td',attrs={"class": "td1"}).a['href']
                xinghao = subsoup.find('td',attrs={"class": "td1"}).img['title']
                
                if  subsoup.find('td',attrs={"class": "td3"}).em is None:
                    xiaoliang = '0'
                else:
                    xiaoliang = subsoup.find('td',attrs={"class": "td3"}).em.string
                  
                if  subsoup.find('td',attrs={"class": "td3"}).strong is None:
                    price = '0'
                else:
                    price = subsoup.find('td',attrs={"class": "td3"}).strong.string                    

                tuhus.append((wangzhi,xinghao, xiaoliang,price))
            
    finally:
        yield from response.release()


def list2file(tuhuslist):
    '''
    保存文件
    '''
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    save_path = os.path.join(sys.path[0], "tuhuguanwang"+yesterday.strftime('%Y%m%d')+".csv")
    f_obj = open(save_path, 'w',encoding='utf-8') # w 表示打开方式
    title = ['网址','轮胎名称', '购买人数','价格']
    html = '\t'.join(title)+ '\n'    
    for luntai in tuhuslist:
        html += '\t'.join(luntai) + '\n'
    f_obj.write(html)
    f_obj.close()



# 爬取得网页
urllist = ['http://item.tuhu.cn/List/Tires.html']  # 要爬取的网页
url = 'http://item.tuhu.cn/List/Tires/'     # 基础网址
page = 13                                  # 总共爬到多少页
for i in range(2,page):
    urllist.append(url+str(i)+'.html')


# 一张张爬取所有轮胎列表
tuhus = []

loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    tasks = [tuhu(url) for url in urllist]
    loop.run_until_complete(asyncio.wait(tasks))
    list2file(tuhus)
    


