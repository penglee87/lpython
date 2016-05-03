#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

@asyncio.coroutine
def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        yield from asyncio.sleep(3)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))

loop = asyncio.get_event_loop()
tasks = [
    asyncio.ensure_future(factorial("A", 2)),
    asyncio.ensure_future(factorial("B", 3)),
    asyncio.ensure_future(factorial("C", 4))]
#tasks = [factorial("A", 2),factorial("B", 3),factorial("C", 4)] 与上面效果相同
"""或者
tasks = [asyncio.Task(factorial("A", 2),loop=loop),
         asyncio.Task(factorial("B", 3), loop=loop),
         asyncio.Task(factorial("C", 4), loop=loop)]
"""

"""取消任务         
for w in tasks:
    print(w)
    w.cancel()
"""
loop.run_until_complete(asyncio.wait(tasks))
loop.close()