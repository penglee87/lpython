#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找出此页面下所有同源host的所有超链接
"""
import asyncio
import time
import logging
import urllib.parse
import aiohttp
import cgi
import re


@asyncio.coroutine
def parse_links(url):
    """parse_links  URL."""
    tries = 0
    exception = None
    seen_urls = set()
    root_domains = set()
    parts = urllib.parse.urlparse(url)
    host, port = urllib.parse.splitport(parts.netloc)
    root_domains.add(host)
    while True:
        try:
            response = yield from session.get(url, allow_redirects=False)  #1
            break  #2
        except aiohttp.ClientError as client_error:
            LOGGER.info('try %r for %r raised %r', tries, url, client_error)
            exception = client_error



    try:  #3
        if response.status in (300, 301, 302, 303, 307):
            location = response.headers['location']

        elif response.status == 200:
            links = set()
            body = yield from response.read()
            content_type = response.headers.get('content-type')
            pdict = {}
            
            if content_type:
                content_type, pdict = cgi.parse_header(content_type)
            
            encoding = pdict.get('charset', 'utf-8')
            if content_type in ('text/html', 'application/xml'):
                text = yield from response.text()
            
                # Replace href with (?:href|src) to follow image links.
                urls = set(re.findall(r'''(?i)href=["']([^\s"'<>]+)''',text))
                for url in urls:
                    normalized = urllib.parse.urljoin(response.url, url)  #根据基础url和另一url组合出新完整url
                    #print(url,'|',normalized)
                    defragmented, frag = urllib.parse.urldefrag(normalized)
                    parts = urllib.parse.urlparse(defragmented) #将url分解成相应片段
                    host, port = urllib.parse.splitport(parts.netloc)
                    if host in root_domains:
                        #print(defragmented)
                        links.add(defragmented)

    finally:
        yield from response.release()
    return links
        

url = 'http://xkcd.com'
loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    links = loop.run_until_complete(parse_links(url))
    print(links)
    
"""改为tasks以后,返回结果会省略很多信息,具体如下
urls=['http://xkcd.com','http://www.163.com/']
tasks = [parse_links(url) for url in urls]
loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    links = loop.run_until_complete(asyncio.wait(tasks))
    print(links)
    
({
<Task finished coro=<parse_links() done, defined at aiohttp_05.py:15> result={'http://xkcd.com/', 'http://xkcd.com/1/', 'http://xkcd.com/150/', 'http://xkcd.com/162/', 'http://xkcd.com/1663/', 'http://xkcd.com/556/', ...}>, 
<Task finished coro=<parse_links() done, defined at aiohttp_05.py:15> result={'http://www.163.com', 'http://www.163.com/', 'http://www.163.com/newsapp/', 'http://www.1...k_window.html', 'http://www.1...page_v13.html', 'http://www.1...m/taidu/2015/', ...}>
}, set())
"""


