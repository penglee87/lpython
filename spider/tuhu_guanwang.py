#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os,sys,requests
import datetime

    
def getHtml(url):
    """
    伪装头部并得到网页内容
    """
    #r = requests.Session()
    #html_bytes = r.get(url)
    html_bytes = requests.get(url)
    html_string = html_bytes.text
    return html_string
    
    
def tuhu(url_content):
    """
    输入网页内容进行轮胎爬取
    返回轮胎信息元组
    """
    tuhus = []
    soup = BeautifulSoup(url_content, 'html.parser') # 开始解析 

    # tuhutable = soup.select('div.indent table div a')
    tuhutable = soup.find_all("tr")  # 找到所有轮胎所在标记

    # 循环遍历轮胎列表
    for tuhu in tuhutable:
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
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    save_path = os.path.join(sys.path[0], "tuhuguanwang"+yesterday.strftime('%Y%m%d')+".csv")
    f_obj = open(save_path, 'w',encoding='utf-8') # w 表示打开方式
    title = ['网址','轮胎名称', '购买人数','价格']
    html = '\t'.join(title)+ '\n'
    for page in tuhuslist:
        for luntai in page:
            html += '\t'.join(luntai) + '\n'
    f_obj.write(html)
    f_obj.close()



# 爬取得网页
urllist = ['http://item.tuhu.cn/List/Tires.html']  # 要爬取的网页
url = 'http://item.tuhu.cn/List/Tires/'     # 基础网址
page = 339                                  # 总共爬到多少页
for i in range(2,page):
    urllist.append(url+str(i)+'.html')


# 一张张爬取所有轮胎列表
tuhuslist = []
for url in urllist:
    html_doc = getHtml(url)  #返回一个网页文本文档
    tuhuslist.append(tuhu(html_doc))
    
list2file(tuhuslist)

