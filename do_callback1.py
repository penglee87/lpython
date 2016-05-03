#!/usr/bin/env python
# coding=utf-8
"""
带额外状态信息的回调函数
"""

def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)

>>> def print_result(result):
...     print('Got:', result)
...
>>> def add(x, y):
...     return x + y
...
>>> apply_async(add, (2, 3), callback=print_result)
Got: 5
>>> apply_async(add, ('hello', 'world'), callback=print_result)
Got: helloworld



#为了让回调函数访问外部信息，一种方法是使用一个绑定方法来代替一个简单函数。 
#比如，下面这个类会保存一个内部序列号，每次接收到一个 result 的时候序列号加1：

class ResultHandler:

    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))
        
        
#使用这个类的时候，你先创建一个类的实例，然后用它的 handler() 绑定方法来做为回调函数：

>>> r = ResultHandler()
>>> apply_async(add, (2, 3), callback=r.handler)
[1] Got: 5
>>> apply_async(add, ('hello', 'world'), callback=r.handler)
[2] Got: helloworld
>>>


#第二种方式，作为类的替代，可以使用一个闭包捕获状态值，例如：

def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler
    
#下面是使用闭包方式的一个例子：

>>> handler = make_handler()
>>> apply_async(add, (2, 3), callback=handler)
[1] Got: 5
>>> apply_async(add, ('hello', 'world'), callback=handler)
[2] Got: helloworld
>>>
#还有另外一个更高级的方法，可以使用协程来完成同样的事情：

def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
        
#对于协程，你需要使用它的 send() 方法作为回调函数，如下所示：

>>> handler = make_handler()
>>> next(handler) # Advance to the yield
>>> apply_async(add, (2, 3), callback=handler.send)
[1] Got: 5
>>> apply_async(add, ('hello', 'world'), callback=handler.send)
[2] Got: helloworld
>>>