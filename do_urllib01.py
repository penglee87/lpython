#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import urllib.request
import urllib
 
from collections import deque
#爬取 http://news.dbanotes.net 及相关页面
queue = deque()
visited = set()
 
url = 'http://news.dbanotes.net'  # 入口页面, 可以换成别的
 
queue.append(url)
cnt = 0
 
while queue:
  url = queue.popleft()  # 队首元素出队
  visited |= {url}  # 标记为已访问
  f = open(r'C:\Users\Administrator\Documents\GitHub\lspider\spider02.txt', 'a') 
  f.write('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url + '\r\n')
  cnt += 1
  '''
  urlop = urllib.request.urlopen(url, timeout = 0, capath=None)
  if 'html' not in urlop.getheader('Content-Type'):
    continue
  '''
  with  urllib.request.urlopen(url, timeout = 0, capath=None) as urlop:
    if 'html' not in urlop.getheader('Content-Type'):
      continue
  
  
  # 避免程序异常中止, 用try..catch处理异常
  try:
    data = urlop.read().decode('utf-8')
  except:
    continue
 
  # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
  linkre = re.compile('href="(.+?)"')
  for x in linkre.findall(data):
    if 'http' in x and x not in visited:
      queue.append(x)
      f.write('加入队列 --->  ' + x + '\r\n')
      
  f.close()
  
  
