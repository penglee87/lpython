import orm
import asyncio
from models import User, Blog, Comment

def test():
    yield from orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='www', password='www', db='awesome')

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    yield from u.save()
'''
for x in test(loop):
    pass
'''
loop = asyncio.get_event_loop()
loop.run_until_complete(test())
#loop.run_forever()