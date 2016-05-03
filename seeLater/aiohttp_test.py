
"""
http://stackoverflow.com/questions/29827642/asynchronous-aiohttp-requests-fails-but-synchronous-requests-succeed
asynchronous aiohttp requests fails, but synchronous requests succeed
"""
import asyncio
import aiohttp
import requests

urls = [
    'http://www.whitehouse.gov/cea/', 
    'http://www.whitehouse.gov/omb', 
    'http://www.google.com']


def test_sync():
    for url in urls:
        r = requests.get(url)
        print(r.status_code)


def test_async():
    for url in urls:
        try:
            r = yield from aiohttp.request('get', url)
        except aiohttp.errors.ClientOSError as e:
            print('bad eternal link %s: %s' % (url, e))
        else:
            print(r.status)


if __name__ == '__main__':
    print('async')
    asyncio.get_event_loop().run_until_complete(test_async())
    print('sync')
    test_sync()
    
    
    
"""    
import asyncio
import aiohttp

urls = [
    'http://www.whitehouse.gov/cea/',
    'http://www.whitehouse.gov/omb',
    'http://www.google.com']


def test_async():
    connector = aiohttp.TCPConnector(verify_ssl=False)
    for url in urls:
        try:
            r = yield from aiohttp.request('get', url, connector=connector)
        except aiohttp.errors.ClientOSError as e:
            print('bad eternal link %s: %s' % (url, e))
        else:
            print(r.status)


if __name__ == '__main__':
    print('async')
    asyncio.get_event_loop().run_until_complete(test_async())
"""