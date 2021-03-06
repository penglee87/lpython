#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A simple web crawler -- main driver program.
提取网页中所有关联链接
合并模块后简化版本
"""

# TODO:
# - Add arguments to specify TLS settings (e.g. cert/key files).

import argparse
import asyncio
import logging
import sys
import cgi
from collections import namedtuple
import re
import time
import urllib.parse

from asyncio import Queue
import aiohttp  # Install with "pip install aiohttp".

LOGGER = logging.getLogger(__name__)
print(LOGGER)
"""Reporting subsystem for web crawler."""



class Stats:
    """Record stats of various sorts."""

    def __init__(self):
        self.stats = {}

    def add(self, key, count=1):
        self.stats[key] = self.stats.get(key, 0) + count

    def report(self, file=None):
        for key, count in sorted(self.stats.items()):
            print('%10d' % count, key, file=file)


def report(crawler, file=None):
    """Print a report on all completed URLs."""
    t1 = crawler.t1 or time.time()
    dt = t1 - crawler.t0
    if dt and crawler.max_tasks:
        speed = len(crawler.done) / dt / crawler.max_tasks
    else:
        speed = 0
    stats = Stats()
    print('*** Report ***', file=file)
    try:
        show = list(crawler.done)
        show.sort(key=lambda _stat: _stat.url)
        for stat in show:
            url_report(stat, stats, file=file)
    except KeyboardInterrupt:
        print('\nInterrupted', file=file)
    print('Finished', len(crawler.done),
          'urls in %.3f secs' % dt,
          '(max_tasks=%d)' % crawler.max_tasks,
          '(%.3f urls/sec/task)' % speed,
          file=file)
    stats.report(file=file)
    print('Todo:', crawler.q.qsize(), file=file)
    print('Done:', len(crawler.done), file=file)
    print('Date:', time.ctime(), 'local time', file=file)


def url_report(stat, stats, file=None):
    """Print a report on the state for this URL.

    Also update the Stats instance.
    """
    if stat.exception:
        stats.add('fail')
        stats.add('fail_' + str(stat.exception.__class__.__name__))
        print(stat.url, 'error', stat.exception, file=file)
    elif stat.next_url:
        stats.add('redirect')
        print(stat.url, stat.status, 'redirect', stat.next_url,
              file=file)
    elif stat.content_type == 'text/html':
        stats.add('html')
        stats.add('html_bytes', stat.size)
        print(stat.url, stat.status,
              stat.content_type, stat.encoding,
              stat.size,
              '%d/%d' % (stat.num_new_urls, stat.num_urls),
              file=file)
    else:
        if stat.status == 200:
            stats.add('other')
            stats.add('other_bytes', stat.size)
        else:
            stats.add('error')
            stats.add('error_bytes', stat.size)
            stats.add('status_%s' % stat.status)
        print(stat.url, stat.status,
              stat.content_type, stat.encoding,
              stat.size,
              file=file)


def lenient_host(host):
    parts = host.split('.')[-2:]
    return ''.join(parts)


def is_redirect(response):
    return response.status in (300, 301, 302, 303, 307)


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


class Crawler:
    """Crawl a set of URLs.

    This manages two sets of URLs: 'urls' and 'done'.  'urls' is a set of
    URLs seen, and 'done' is a list of FetchStatistics.
    """
    def __init__(self, roots,
                 exclude=None, strict=True,  # What to crawl.
                 max_redirect=10, max_tries=4,  # Per-url limits.
                 max_tasks=10, *, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.roots = roots
        self.exclude = exclude
        self.strict = strict
        self.max_redirect = max_redirect
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.q = Queue(loop=self.loop)
        self.seen_urls = set()
        self.done = []
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.root_domains = set()
        for root in roots:
            parts = urllib.parse.urlparse(root)
            host, port = urllib.parse.splitport(parts.netloc)
            if not host:
                continue
            if re.match(r'\A[\d\.]*\Z', host):
                self.root_domains.add(host)
            else:
                host = host.lower()
                if self.strict:
                    self.root_domains.add(host)
                else:
                    self.root_domains.add(lenient_host(host))
        for root in roots:
            self.add_url(root)
        self.t0 = time.time()
        self.t1 = None

    def close(self):
        """Close resources."""
        self.session.close()

    def host_okay(self, host):
        """Check if a host should be crawled.

        A literal match (after lowercasing) is always good.  For hosts
        that don't look like IP addresses, some approximate matches
        are okay depending on the strict flag.
        """
        host = host.lower()
        if host in self.root_domains:
            return True
        if re.match(r'\A[\d\.]*\Z', host):
            return False
        if self.strict:
            return self._host_okay_strictish(host)
        else:
            return self._host_okay_lenient(host)

    def _host_okay_strictish(self, host):
        """Check if a host should be crawled, strict-ish version.

        This checks for equality modulo an initial 'www.' component.
        """
        host = host[4:] if host.startswith('www.') else 'www.' + host
        return host in self.root_domains

    def _host_okay_lenient(self, host):
        """Check if a host should be crawled, lenient version.

        This compares the last two components of the host.
        """
        return lenient_host(host) in self.root_domains

    def record_statistic(self, fetch_statistic):
        """Record the FetchStatistic for completed / failed URL."""
        self.done.append(fetch_statistic)

    @asyncio.coroutine
    def parse_links(self, response):
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
                    if self.url_allowed(defragmented):
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
    def fetch(self, url, max_redirect):
        """Fetch one URL."""
        tries = 0
        exception = None
        while tries < self.max_tries:
            try:
                response = yield from self.session.get(url, allow_redirects=False)  #1
                break  #2
            except aiohttp.ClientError as client_error:
                LOGGER.info('try %r for %r raised %r', tries, url, client_error)
                exception = client_error
        else:
            return
            
        try:
            if is_redirect(response):
                location = response.headers['location']

            else:  #4
                stat, links = yield from self.parse_links(response)
                self.record_statistic(stat)
                for link in links.difference(self.seen_urls):
                    self.q.put_nowait((link, self.max_redirect))
                self.seen_urls.update(links)
        finally:
            yield from response.release()

    @asyncio.coroutine
    def work(self):
        """Process queue items forever."""
        try:
            while True:
                url, max_redirect = yield from self.q.get()  #q.get() Remove and return an item from the queue. If queue is empty, wait until an item is available.
                #print('url',url, 'max_redirect', max_redirect)
                assert url in self.seen_urls   #assert 断言,异常会直接抛出
                yield from self.fetch(url, max_redirect)
                self.q.task_done()  #Indicate that a formerly enqueued task is complete.表明以前排队的任务完成
        except asyncio.CancelledError:
            pass

    def url_allowed(self, url):
        if self.exclude and re.search(self.exclude, url):
            return False
        parts = urllib.parse.urlparse(url)
        if parts.scheme not in ('http', 'https'):
            LOGGER.debug('skipping non-http scheme in %r', url)
            return False
        host, port = urllib.parse.splitport(parts.netloc)
        if not self.host_okay(host):
            LOGGER.debug('skipping non-root host in %r', url)
            return False
        return True

    def add_url(self, url, max_redirect=None):
        """Add a URL to the queue if not seen before."""
        if max_redirect is None:
            max_redirect = self.max_redirect
        LOGGER.debug('adding %r %r', url, max_redirect)
        self.seen_urls.add(url)
        self.q.put_nowait((url, max_redirect))  #put_nowait() Put an item into the queue without blocking.此句实际最先执行

    @asyncio.coroutine
    def crawl(self):
        """Run the crawler until all finished."""
        workers = [asyncio.Task(self.work(), loop=self.loop) for _ in range(self.max_tasks)]
        self.t0 = time.time()
        yield from self.q.join()  #Block until all items in the queue have been gotten and processed.保持阻塞状态,直到处理了队列中的所有项目为止
        self.t1 = time.time()
        for w in workers:
            w.cancel()


ARGS = argparse.ArgumentParser(description="Web crawler")

ARGS.add_argument(
    'roots', nargs='*',
    default=[], help='Root URL (may be repeated)')

ARGS.add_argument(
    '-q', '--quiet', action='store_const', const=0, dest='level',
    default=2, help='Only log errors')


def fix_url(url):
    """Prefix a schema-less URL with http://."""
    if '://' not in url:
        url = 'http://' + url
    return url


def main():
    """Main program.

    Parse arguments, set up event loop, run crawler, print report.
    """
    args = ARGS.parse_args()
    print(args)
    if not args.roots:
        print('Use --help for command line help')
        return

    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=levels[min(args.level, len(levels)-1)])   #实际未打印结果

    loop = asyncio.get_event_loop()

    roots = {fix_url(root) for root in args.roots}
    
    #创建crawler实例时,实现了add_url操作
    crawler = Crawler(roots)
    try:
        loop.run_until_complete(crawler.crawl())  # Crawler gonna crawl.
    except KeyboardInterrupt:
        sys.stderr.flush()
        print('\nInterrupted\n')
    finally:
        report(crawler)   #实际输出语句
        crawler.close()   #必须关闭

        # next two lines are required for actual aiohttp resource cleanup
        #loop.stop()
        #loop.run_forever()

        loop.close()


if __name__ == '__main__':
    main()


#python crawl_01.py -q xkcd.com > xkcd01.txt