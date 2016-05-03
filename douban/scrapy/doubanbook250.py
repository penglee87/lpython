# -*- coding:utf-8 -*-
# 爬取 http://book.douban.com/top250?icn=index-book250-all
# http://book.douban.com/top250?start=0,25,50
# 生成excel http://www.jb51.net/article/42635.htm
# 读取excel http://blog.chinaunix.net/uid-21222282-id-3420444.html
#     Python2.x才可以运行
from bs4 import BeautifulSoup
from tool.gethtml import getHtml
# from pyExcelerator import Workbook
import os, urllib.request
# 保存的图书封面
localPath='web/image'


# 根据文件名创建文件
def createFileWithFileName(localPathParam,fileName):
    totalPath=localPathParam+'/'+fileName+'.jpg'
    if not os.path.exists(totalPath):
        file=open(totalPath,'a+')
        file.close()
        return totalPath


# 根据图片的地址，下载图片并保存在本地
def getAndSaveImg(imgUrl, fileName):
    if(len(imgUrl)!= 0):
        urllib.request.urlretrieve(imgUrl,createFileWithFileName(localPath,fileName))
        #local_filename, headers = urllib.request.urlretrieve(url, filename=None, reporthook=None, data=None)


def book(url_content):
    """
    输入网页内容进行图书爬取
    返回图书信息元组

    """
    books = []
    soup = BeautifulSoup(url_content, 'html.parser') # 开始解析 

    # booktable = soup.select('div.indent table div a')
    booktable1 = soup.find_all("table", attrs={"width": "100%"})  # 找到所有图书所在标记

    # 循环遍历图书列表
    for book in booktable1:
        simplebook = book
        # print(simplebook)

        subsoup = BeautifulSoup(str(simplebook), 'html.parser') # 单本书进行解析
        # print(subsoup)

        # 图书封面：
        # http://img4.doubanio.com/spic/s1237549.jpg
        # http://img4.doubanio.com/lpic/s1237549.jpg
        booksmallimg = subsoup.img['src']
        imgtemp = booksmallimg.split('/')
        imgtemp[len(imgtemp)-2] = 'lpic'
        booklargeimg = '/'.join(imgtemp)
        # print(booksmallimg)
        # print(booklargeimg)

        # 图书信息
        # print(subsoup.div)
        # print(subsoup.div.a)
        booklink = subsoup.div.a['href']  # 图书链接：http://book.douban.com/subject/1084336/
        bookname1 = subsoup.div.a['title'] # 图书名称：小王子

        # 下载图片
        getAndSaveImg(booklargeimg, bookname1)

        bookname2t = subsoup.div.span
        if bookname2t:
            bookname2 = bookname2t.string
        else:
            bookname2 = ''
        # 图书别称：Le Petit Prince

        bookinfo = subsoup.p.string # 图书出版信息：[法] 圣埃克苏佩里 / 马振聘 / 人民文学出版社 / 2003-8 / 22.00元

        bookstar = subsoup.find('span',attrs={"class": "rating_nums"}).string # 图书星级：9.0
        bookcommentnum = subsoup.find('span',attrs={"class": "pl"}).string.strip('\r\n ()人评价') # 评价人数：190325

        books.append((bookname1, bookname2, booklink, booklargeimg, bookinfo, bookstar, bookcommentnum))
    # 返回图书列表
    return books

# 本地测试所用
# booklist = book(open("web/douban250.html",'rb').read())
# print(booklist)

# 爬取得网页
urllist = []                                     # 要爬取的网页
url = 'http://book.douban.com/top250?start='     # 基础网址
page = 10                                         # 总共爬10页
pagesize = 25                                    # 每页25本
for i in range(page):
    urllist.append(url+str(i*pagesize))
# print(urllist)

# 一张张爬取所有图书列表
bookslist = []
for url in urllist:
    html_doc = getHtml(url)  #返回一个  'utf-8' 网页文本文档
    bookslist.append(book(html_doc))


# # 存入Exexl
# w = Workbook()     #创建一个工作簿
# ws = w.add_sheet('图书')     #创建一个工作表
# ws.write(0,0,'最热图书250本')
# ws.write(1,0,'序号')
# ws.write(1,1,'图书名称')
# ws.write(1,2,'图书别称')
# ws.write(1,3,'图书链接')
# ws.write(1,4,'图书封面')
# ws.write(1,5,'图书出版信息')
# ws.write(1,6,'图书星数')
# ws.write(1,7,'图书评论数')
#
# i = 2
# for page in bookslist:
#     for book in page:
#         ws.write(i,0,i-1)
#         ws.write(i,1,book[0])
#         ws.write(i,2,book[1])
#         ws.write(i,3,book[2])
#         ws.write(i,4,book[3])
#         ws.write(i,5,book[4])
#         ws.write(i,6,book[5])
#         ws.write(i,7,book[6])
#
# w.save('web/book.xls')     #保存

# print(bookslist)
# print(len(bookslist))

# 编码问题 ：http://blog.csdn.net/greatpresident/article/details/8209712
fout = open('web/book.csv', 'w',encoding='utf-8')  # 必须加上编码，写入到文件
title = ['图书名称','图书别称', '图书链接', '图书封面', '图书出版信息', '图书星数', '图书评论数']
html = ','.join(title)+ '\n'
for page in bookslist:
    for book in page:
        html += ','.join(book) + '\n'
# print(html)
fout.write(html)
fout.close()


# 生成的csv默认为ASCII编码，用记事本打开另存为ASCII编码，然后打开再转Excel等