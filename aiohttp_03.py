#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
作者：柯豪
链接：https://www.zhihu.com/question/38202077/answer/75930426
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
import aiohttp
import asyncio
import requests
import time


def timing(f):
    """function timing wrapper"""

    def wrapper(*arg, **kw):
        t1 = time.time()
        ret = f(*arg, **kw)
        t2 = time.time()
        print('took: %2.4f sec: func:%r args:[%r, %r] ' % (t2 - t1, f.__name__, arg, kw))
        return ret

    return wrapper


@timing
def using_aiohttp(urls):
    async def process_one_url(url):
        print("aiohttp send request")
        r = await aiohttp.get(url)
        print("aiohttp get response %s" % r.status)
        r.close()

    loop = asyncio.get_event_loop()
    tasks = asyncio.gather(*[process_one_url(url) for url in urls])
    loop.run_until_complete(tasks)
    #tasks = [process_one_url(url) for url in urls]
    #loop.run_until_complete(asyncio.wait(tasks))


@timing
def using_requests(urls):
    for url in urls:
        print("requests send request")
        r = requests.get(url)
        print("requests get response %s" % r.status_code)


def main():
    urls = ["http://www.sina.com.cn"] * 10
    using_aiohttp(urls)
    using_requests(urls)


if __name__ == "__main__":
    main()

"""
结果比较：
aiohttp send request
aiohttp send request
aiohttp send request
...
aiohttp get response 200
aiohttp get response 200
aiohttp get response 200
...
took: 18.4507 sec: func:'using_aiohttp' args:...), {}] 
requests send request
requests get response 200
requests send request
requests get response 200
requests send request
requests get response 200
...
took: 151.074 sec: func:'using_requests' args:...), {}] 

"""