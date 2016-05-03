#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尝试消除类1
"""
import re
import asyncio
from asyncio import Queue
import time
import logging
import urllib.parse
import aiohttp
from collections import namedtuple

FetchStatistic = namedtuple('FetchStatistic',
                            ['url',
                             'next_url',
                             'status',
                             'exception',
                             'size',
                             'content_type',
                             'encoding',
                             'num_urls',
                             'num_new_urls'])

@asyncio.coroutine
def parse_links(response):
    """Return a FetchStatistic and list of links."""
    links = set()
    content_type = None
    encoding = None
    body = yield from response.read()

    if response.status == 200:
        content_type = response.headers.get('content-type')
        pdict = {}

        if content_type:
            content_type, pdict = cgi.parse_header(content_type)

        encoding = pdict.get('charset', 'utf-8')
        if content_type in ('text/html', 'application/xml'):
            text = yield from response.text()

            # Replace href with (?:href|src) to follow image links.
            urls = set(re.findall(r'''(?i)href=["']([^\s"'<>]+)''',text))
            if urls:
                LOGGER.info('got %r distinct urls from %r',len(urls), response.url)
            for url in urls:
                normalized = urllib.parse.urljoin(response.url, url)
                defragmented, frag = urllib.parse.urldefrag(normalized)
                parts = urllib.parse.urlparse(defragmented)
                host, port = urllib.parse.splitport(parts.netloc)
                if host in root_domains:
                    links.add(defragmented)

    stat = FetchStatistic(
        url=response.url,
        next_url=None,
        status=response.status,
        exception=None,
        size=len(body),
        content_type=content_type,
        encoding=encoding,
        num_urls=len(links),
        num_new_urls=len(links - self.seen_urls))

    return stat, links

@asyncio.coroutine
def fetch(url, max_redirect):
    """Fetch one URL."""
    tries = 0
    exception = None
    while tries < max_tries:
        try:
            response = yield from session.get(url, allow_redirects=False)  #1
            break  #2
        except aiohttp.ClientError as client_error:
            LOGGER.info('try %r for %r raised %r', tries, url, client_error)
            exception = client_error
    else:
        return

    try:  #3
        if response.status in (300, 301, 302, 303, 307):
            location = response.headers['location']
        else:  #4
            stat, links = yield from parse_links(response)
            done.append(stat)
            for link in links.difference(seen_urls):
                q.put_nowait((link, max_redirect))
            seen_urls.update(links)
    finally:
        yield from response.release()
        

@asyncio.coroutine
def work():
    """Process queue items forever."""
    try:
        while True:
            url, max_redirect = yield from q.get()
            assert url in seen_urls
            yield from fetch(url, max_redirect)
            #yield from asyncio.sleep(3)
            q.task_done()
    except asyncio.CancelledError:
        pass

@asyncio.coroutine
def crawl():
    """Run the crawler until all finished."""
    workers = [asyncio.Task(work(), loop=loop) for _ in range(max_tasks)]
    t0 = time.time()
    yield from q.join()  #Block until all items in the queue have been gotten and processed.保持阻塞状态,直到处理了队列中的所有项目为止
    t1 = time.time()
    for w in workers:
        w.cancel()
        
def add_url(url, max_redirect=None):
    """Add a URL to the queue if not seen before."""
    if max_redirect is None:
        max_redirect = max_redirect
    LOGGER.debug('adding %r %r', url, max_redirect)
    seen_urls.add(url)
    q.put_nowait((url, max_redirect))  #put_nowait() Put an item into the queue without blocking.此句实际最先执行
    
    
   
done = []      
max_tasks = 10  
max_tries=4
max_redirect=10    
loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)
q = Queue(loop=loop)
seen_urls = set()
root_domains = set()
LOGGER = logging.getLogger(__name__)
#url = 'http://xkcd.com'
roots=['http://xkcd.com']
for root in roots:
    parts = urllib.parse.urlparse(root)
    host, port = urllib.parse.splitport(parts.netloc)
    if not host:
        continue
    if re.match(r'\A[\d\.]*\Z', host):
        root_domains.add(host)
    else:
        host = host.lower()
        root_domains.add(host)
        
for root in roots:
    add_url(root)


try:
    loop.run_until_complete(crawl())  # Crawler gonna crawl.
except KeyboardInterrupt:
    sys.stderr.flush()
    print('\nInterrupted\n')
finally:
    #report(crawler)
    session.close()

    # next two lines are required for actual aiohttp resource cleanup
    #loop.stop()
    #loop.run_forever()

    loop.close()


#python crawl_02.py  > xkcd02.txt