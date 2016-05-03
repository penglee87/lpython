#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os,sys,re,requests
import datetime


def tuhu(url):
    """
    输入网页内容进行门店爬取
    返回门店信息元组
    """
    tuhus = []
    html_bytes = requests.get(url)
    url_content = html_bytes.text
    soup = BeautifulSoup(url_content, 'html.parser') # 开始解析 

    # tuhutable = soup.select('div.indent table div a')
    
    #province = soup.find(id="step1").string  # 找到省份名称
    province_name = re.search(r'<a href="javascript:void\(0\);" class="active">(.*?)</a>',url_content).group(1)
    city_name = re.search(r'<a href="javascript:void\(0\);">(.*?)</a>',url_content).group(1)

    tuhutable = soup.find_all("div" ,class_="item clearfix")  # 找到所有门店所在标记


    # 循环遍历门店列表
    for tuhu in tuhutable:
        simpletuhu = str(tuhu)
        subsoup = BeautifulSoup(simpletuhu, 'html.parser')
        
        wangzhi = subsoup.find('a',attrs={"class": "carparname"})['href']
        shopname = subsoup.find('a',attrs={"class": "carparname"})['title']
        shop_level = subsoup.find('div',attrs={"class": "shop-level"}).span.string
        #shop_type = subsoup.find('span',attrs={"class": re.compile("i-shop shop")})['title']
        '''
        if subsoup.find('span',attrs={"class": "i-shop shop-dian"}):
            shop_type = subsoup.find('span',attrs={"class": "i-shop shop-dian"})['title']
        else: shop_type='none'
        '''
        if subsoup.find('span',attrs={"class": "i-shop shop-dian"}):
            shop_type = '快修店'
        elif subsoup.find('span',attrs={"class": "i-shop shop-xiu"}):
            shop_type = '修理厂'
        else: shop_type = '4S店'
        
        
        
        if subsoup.find('span',attrs={"class": "install-num"}).i:
            install_num = subsoup.find('span',attrs={"class": "install-num"}).i.string
        else: install_num = '0'
        
        if re.search(r'<span>评价<i>(.*?)</i></span>',simpletuhu):
            shop_grade = re.search(r'<span>评价<i>(.*?)</i></span>',simpletuhu).group(1)
        else: shop_grade = '0'
        
        if re.search(r'<p class="address"><span class="label">门店地址：</span><span title=(.*?)>(.*?)</span></p>',simpletuhu):
            address = re.search(r'<p class="address"><span class="label">门店地址：</span><span title=(.*?)>(.*?)</span></p>',simpletuhu).group(1)
        #address = subsoup.find('p',attrs={"class": "address"}).span.string
        if re.search('支付宝',simpletuhu):payment1 = '1' 
        else:payment1 = '0'
        if re.search('刷卡',simpletuhu):payment2 = '1' 
        else:payment2 = '0'
        if re.search('现金',simpletuhu):payment3 = '1' 
        else:payment3 = '0'


        
        '''   
        if  subsoup.find('td',attrs={"class": "td3"}).em is None:
            xiaoliang = '0'
        else:
            xiaoliang = subsoup.find('td',attrs={"class": "td3"}).em.string
          
        if  subsoup.find('td',attrs={"class": "td3"}).strong is None:
            price = '0'
        else:
            price = subsoup.find('td',attrs={"class": "td3"}).strong.string
            
        
        f = subsoup.find(...)
        if not f:
            price = 0
        else:
            price = f.strong.string
        '''

        tuhus.append((province_name,city_name,wangzhi,shopname,shop_level,shop_type,install_num,shop_grade,address,payment1,payment2,payment3))
    # 返回门店列表
    return tuhus
    
    
def get_city_url(province_url):
    url_list = []
    html_bytes = requests.get(province_url)
    html_string = html_bytes.text
    soup = BeautifulSoup(html_string, 'html.parser') # 开始解析 
    url_table = soup.find_all("ul" ,class_="tab-content")
    subsoup = BeautifulSoup(str(url_table), 'html.parser')
    url_table2 = subsoup.find_all("a")
    for u in url_table2:
        subsubsoup = BeautifulSoup(str(u), 'html.parser')
        subsuburl = subsubsoup.find("a")['href']
        url_list.append(subsuburl)
    return url_list


def saveFile(tuhuslist):
    '''
    保存文件
    '''
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    save_path = os.path.join(sys.path[0], "tuhushopscity"+yesterday.strftime('%Y%m%d')+".csv")
    f_obj = open(save_path, 'w',encoding='utf-8') # w 表示打开方式
    title = ['省份','城市','网址','门店名称','门店等级','门店类型','安装数','门店评价','门店地址','支付宝','刷卡','现金']
    html = '|'.join(title)+ '\n'
    for page in tuhuslist:
        for luntai in page:
            html += '|'.join(luntai) + '\n'
    f_obj.write(html)
    f_obj.close()



# 爬取得网页
url = 'http://www.tuhu.cn/Shops/'     # 基础网址
#url = 'http://www.tuhu.cn/Shops/2344.aspx'     # 基础网址
province_urllist=[]
citys_urllist=[]
provinces_id = [1,2,19,20,23,24,25,26,27,28,29,30,31,90,334,407,712,723,724,831,832,978,979,1060,1182,1404,1561,1676,1847,1848,2344]
#provinces_id = [1,23]
dian_list = []
for i in provinces_id:
    province_url=url+str(i)+'.aspx'
    city_urllist = get_city_url(province_url)
    for city_url in city_urllist:
        city_dian = tuhu(city_url)
        dian_list.append(city_dian)

    

    
saveFile(dian_list)

