#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#一些可用变量
import asyncio
import aiohttp
import cgi

async def fetch_page(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            print('response.status',response.status)
            print(response.headers['CONTENT-TYPE'])
            content_type = response.headers.get('content-type')
            print('content_type',content_type)
            pdict = {}
            content_type, pdict = cgi.parse_header(content_type)
            encoding = pdict.get('charset', 'utf-8')
            print('encoding',encoding)
            print(response.url)
            assert response.status == 200
            return await response.read()

loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    content = loop.run_until_complete(fetch_page(session, 'https://api.github.com/events'))
    #print(content)
    
    
    
"""
import asyncio
import aiohttp

async def fetch_page(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            print('response.status',response.status)
            assert response.status == 404
            return await response.read()

loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    content = loop.run_until_complete(fetch_page(session, 'https://api.github.com/event'))
    #print(content)
"""