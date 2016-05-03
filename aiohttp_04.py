#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import aiohttp

def fetch(url):
    """Fetch one URL."""
    tries = 0

    while tries < max_redirect:
        try:
            print('tries',tries)
            tries = tries + 1
            response = yield from aiohttp.get(url, allow_redirects=False) #与区别 aiohttp.ClientSession(loop=asyncio.get_event_loop()).get(url)
            print("aiohttp get response %s" % response.status)
            print(response.text())  #只能返回协程名称 <generator object ClientResponse.text at 0x02F3D5D0>
            response.close()
            if tries > 1:
                print(2)

            break  #2 跳出整个while语句,不会执行后面的else
        except aiohttp.ClientError as client_error:
            LOGGER.info('try %r for %r raised %r', tries, url, client_error)
            exception = client_error
            print(exception)
        
    else:
        # We never broke out of the loop: all tries failed.
        
        print('else')
        return
        
    print('out')   

#tries = 0  一定要定义在任务体内
max_redirect=2 
urls=['http://xkcd.com']*3
loop = asyncio.get_event_loop()
tasks = [fetch(url) for url in urls]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

"""
max_redirect=2 
url='http://xkcd.com'
loop = asyncio.get_event_loop()
loop.run_until_complete(fetch(url))
loop.close()
""" 