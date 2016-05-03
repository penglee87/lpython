"""
作者：阿托
链接：https://www.zhihu.com/question/40985878/answer/91907442
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
import pymysql
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:xxxx@localhost/test',
                       pool_size=10, max_overflow=0)

#test wsgi applicaion with db
def test_example():
    cn = engine.connect()
    rs = cn.execute("select * from users")
    r = rs.fetchone()
    result = r[0]
    rs.close()
    cn.close()
    return str(result)
    
def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)
    r=test_example()
    return [b'hello world' + r.encode()]