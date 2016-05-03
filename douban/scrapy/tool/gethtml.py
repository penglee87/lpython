# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import urllib.request, urllib.parse, http.cookiejar
from bs4 import BeautifulSoup
__author__ = 'hunterhug'


def getHtml(url):
    """
    伪装头部并得到网页内容

    """
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),
                         ('Cookie', '4564564564564564565646540')]

    urllib.request.install_opener(opener)  #安装为默认浏览器，使之后的 urlopen方法可直接调用

    html_bytes = urllib.request.urlopen(url).read()  #urlopen
    html_string = html_bytes.decode('utf-8')
    return html_string


def getSoup(html_content,parse='html.parser'):
    """
    得到网页解析后的对象，方便分拆数据

    """
    return BeautifulSoup(html_content,parse)