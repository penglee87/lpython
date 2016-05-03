"""
作者：阿托
链接：https://www.zhihu.com/question/40985878/answer/91907442
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
import sys
import asyncio
from aiohttp import web

import aiomysql

@asyncio.coroutine
def test_example(request):
    with (yield from request.app['DBPOOL']) as cn:
        cur = yield from cn.cursor()
        yield from cur.execute("select * from users")
        r = yield from cur.fetchone()
        result = r[0]
        yield from cur.close()
    return str(result)
    
@asyncio.coroutine
def hello(request):
    r = yield from test_example(request)
    return web.Response(body=b"hello world" + r.encode())
    
@asyncio.coroutine
def on_cleanup(app):
    pool = app['DBPOOL']
    pool.close()
    yield from pool.wait_closed()

@asyncio.coroutine
def create_app(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', hello)
    app['DBPOOL'] = yield from aiomysql.create_pool(host='localhost',
                                                    user='root',
                                                    password='xxxx',
                                                    db='test',
                                                    minsize=10,
                                                    maxsize=10,
                                                    loop=loop)
                                         
    app.on_cleanup.append(on_cleanup)
    return app

loop = asyncio.get_event_loop()
app = loop.run_until_complete(create_app(loop))

if __name__ == '__main__':
    web.run_app(app, port= (len(sys.argv) > 1 and sys.argv[1]) or 9000)


