#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage  

import os,sys
import datetime

today = datetime.date.today()
yester = today - datetime.timedelta(days=1)
s_yester = yester.strftime('%Y%m%d')
t_yester = yester.strftime('%Y-%m-%d')


from impala.dbapi import connect
conn=connect(host='115.236.185.157', port=2561, use_ssl=True, auth_mechanism='PLAIN', user='***', password='***')
cur=conn.cursor()


s_sql='''
select o.no,o.pay_time,og.sku_code,og.goods_name,sb.brand_name,gd.second_category_name,
og.sale_cost,og.sale_num,uc.money
from
(select * from dbs.src_qccr_orders_all where pt='%s' and status>=6  and channel=0 and source in(1,2,3) and pay_time>='%s') o
inner join(select * from dbs.src_qccr_order_goods where pt='%s' ) og on o.id=og.order_id
inner join (select distinct second_category_id,second_category_name  from dmn.dmn_sku_category_d where pt='%s'
        and first_category_id in(96226,96230,96234,97222,97234)) gd on gd.second_category_id = og.category_id
left join (select * from dbs.src_item_ic_sku where pt='%s' and status=1) sk on og.sku_code=sk.sku_code
left join (select * from dbs.src_item_ic_brand where pt='%s' and status=1) sb on sk.brand_id=sb.brand_id
left join (select * from dbs.src_qccr_user_coupon where pt='%s' ) uc on  uc.use_order_no=o.no '''%(s_yester,t_yester,s_yester,s_yester,s_yester,s_yester,s_yester)

cur.execute(s_sql)
values=cur.fetchall()
cur.close()
conn.close()

    
def saveFile(values):
    f_obj = open('chepin.csv', 'w') # w 表示打开方式
    title = ['no','pay_time','sku_code','goods_name','brand_name','second_category_name','sale_cost','sale_num','money']
    col = '\t'.join(title)+ '\n'
    for v in values:
        col += '\t'.join([str(i) for i in v]) + '\n'
    f_obj.write(col)
    f_obj.close()

saveFile(values)

from_addr = 'lipeng@qccr.com'
password = 'Qc000000'
#to_addr = 'lipeng@qccr.com'
to_addr = ['lipeng@qccr.com','zhangluo@qccr.com']

msg = MIMEMultipart('alternative')  
msg['Subject'] = '每日车品'+s_yester

#att_name = datetime.date.today().strftime('%Y%m%d')+".csv"
att = MIMEText(open('chepin.csv', 'rb').read(), 'base64', 'utf-8')  
att["Content-Type"] = 'application/octet-stream'  
att["Content-Disposition"] = 'attachment; filename="chepin.csv"'  
#att["Content-Disposition"] = 'attachment; filename=att_name'  
msg.attach(att)  



smtp = smtplib.SMTP()  
smtp.connect('smtp.exmail.qq.com')  
smtp.login(from_addr, password)  
smtp.sendmail(from_addr, to_addr, msg.as_string())  
smtp.quit()  

