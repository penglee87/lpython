#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task exception was never retrieved 问题
"""
import asyncio

@asyncio.coroutine
def comain():
    raise SystemExit(2)

def main():
    loop = asyncio.get_event_loop()
    task = loop.create_task(comain())
    try:
        loop.run_until_complete(task)
    except SystemExit:
        print("caught SystemExit!")
        task.exception()   #why
        raise
    finally:
        loop.close()

if __name__ == "__main__":
    main()
    
    
"""
import asyncio

@asyncio.coroutine
def comain():
    raise SystemExit(2)

@asyncio.coroutine
def another():
    try:
        yield from comain()
    except SystemExit:
        print ("consumed")

def main():
    loop = asyncio.get_event_loop()
    task = loop.create_task(another())
    try:
        loop.run_until_complete(task)
    except SystemExit:
        print("caught SystemExit!")
        raise
    finally:
        loop.close()

if __name__ == "__main__":
    main()
    
    
"""