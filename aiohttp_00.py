#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# await cannot be used in global context but inside `async def` only.
import asyncio
import aiohttp

async def fetch_page(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            assert response.status == 200
            return await response.read()

loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    content = loop.run_until_complete(fetch_page(session, 'http://python.org'))
    print(content)
    
""" 
aiohttp.ClientSession(loop=asyncio.get_event_loop()).get(url)
aiohttp.get(url)
区别？    
"""

"""适应3.4版本
import asyncio
import aiohttp

@asyncio.coroutine
def fetch_page(session, url):
    with aiohttp.Timeout(10):
        response =  yield from session.get(url)
        assert response.status == 200
        try:
            content = yield from response.read()
        finally:
            yield from response.release()
        return content
        

loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    content = loop.run_until_complete(fetch_page(session, 'http://www.python.org/'))
    print(content)
    
try:
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop) 
    content = loop.run_until_complete(fetch_page(session, 'http://www.python.org/'))
    print(content)
finally:
    session.close()
    
    
大致上await和yield from是相似的。
使用async def的函数中使用await
使用@asyncio.coroutine装饰器定义的协程中使用yield from
async with语法使用新的异步上下文管理器（Asynchronous Context Managers）协议，没有等价的写法。


#多任务无法返回完整结果
import asyncio
import aiohttp

@asyncio.coroutine
def fetch_page(session, url):
    s = set()
    with aiohttp.Timeout(10):
        response =  yield from session.get(url)
        assert response.status == 200
        try:
            content = yield from response.read()
        finally:
            yield from response.release()
        s.add(content)
        return s
        
try:
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop) 
    tasks = [fetch_page(session, 'http://www.python.org/'),fetch_page(session, 'http://www.sina.com.cn/')]
    content = loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print(str(content))
finally:
    session.close()
"""
    
