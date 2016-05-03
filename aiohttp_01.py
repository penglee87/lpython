#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import aiohttp
#import aiohttp.StreamReader


async def feed_stream(resp, stream):
    h = hashlib.sha256()

    while True:
        chunk = await resp.content.readany()
        if not chunk:
            break
        h.update(chunk)
        s.feed_data(chunk)

    return await h.hexdigest()

loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    resp = session.get('http://httpbin.org/post')
    stream = aiohttp.StreamReader()
    loop.create_task(session.post('http://httpbin.org/post', data=stream))

    file_hash =  feed_stream(resp, stream)