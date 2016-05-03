#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import requests
"""
requests 对象不能用来 yield from
"""

@asyncio.coroutine 
def fetch(url):
    tries = 0
    while tries < max_redirect:
        try:
            print('tries',tries)
            tries = tries + 1
            response = yield from aiohttp.get(url)  #区别 aiohttp.ClientSession(loop=asyncio.get_event_loop()).get(url)
            print("aiohttp get response %s" % response.status)
            #response.close()
            """
            response = yield from requests.get(url)  #出错,跳转至 except
            print(1)
            print(response.status_code)
            response.close()
            """
            if tries > 1:
                print(2)
            #break  # 跳出整个while语句,不会执行后面的else
        except :
            print('exception')
        finally:
            yield from response.release()
        
    else:
        # We never broke out of the loop: all tries failed.
        
        print('else')
        #return
        
    print('out')   
 
#tries = 0
max_redirect=2 
urls=['http://xkcd.com']*4
loop = asyncio.get_event_loop()
tasks = [fetch(url) for url in urls]
loop.run_until_complete(asyncio.wait(tasks))
#tasks.exception()
loop.close()
