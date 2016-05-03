#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

@asyncio.coroutine
def hello_world():
    print("Hello World!")
    yield from asyncio.sleep(3)
    print("Hello again!")
    
loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done

tasks = [hello_world(), hello_world()]
loop.run_until_complete(asyncio.wait(tasks))
"""
tasks = [asyncio.Task(hello_world(), loop=loop) for _ in range(3)]  
loop.run_until_complete(asyncio.wait(tasks))  #仍然要用asyncio.wait
"""
loop.close()

"""
import asyncio

def hello_world(loop):
    print('Hello World')
    loop.stop()

loop = asyncio.get_event_loop()

# Schedule a call to hello_world()
loop.call_soon(hello_world, loop)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()
"""
############################################
"""
#不报错,但无打印结果
import asyncio

@asyncio.coroutine
def hello_world():
    print("Hello World!")
    yield from asyncio.sleep(3)
    print("Hello again!")

@asyncio.coroutine
def tasklist():
    tasks = [asyncio.Task(hello_world(), loop=loop) for _ in range(3)]
    for t in tasks:
        t.cancel()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(tasklist())
loop.close()
"""