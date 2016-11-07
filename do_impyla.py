#!/usr/bin/env python2
# -*- coding: utf-8 -*-



from impala.dbapi import connect
conn=connect(host='115.236.185.157', port=2561, use_ssl=True, auth_mechanism='PLAIN', user='***', password='***')
cur=conn.cursor()
cur.execute("select * from dbs.src_crm_t_store where pt='20161025'  limit 2")
value=cur.fetchall()
print value


'''
ubuntu 下安装 impyla

Dependencies

Required:

Python 2.6+ or 3.3+

six, bit_array

thrift (on Python 2.x) or thriftpy (on Python 3.x)

For Hive and/or Kerberos support:

pip install thrift_sasl
pip install sasl
Optional:

pandas for conversion to DataFrame objects; but see the Ibis project instead

sqlalchemy for the SQLAlchemy engine

pytest for running tests; unittest2 for testing on Python 2.6

Installation

Install the latest release (0.13.1) with pip:

pip install impyla

安装 impyla 时，提示 error: command 'gcc' failed with exit status 1
以下方法可解决
sudo apt-get  build-dep  gcc
for python2 use:
sudo apt-get install python-dev 
for python3 use:
sudo apt-get install python3-dev

sudo apt-get install libsasl2-dev

'''