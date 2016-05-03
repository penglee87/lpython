#!/usr/bin/env python
#-*-coding:utf-8-*-
 
import re
import codecs
 
def matcher(line):
    reg=r'<em>(.*?)<\\/em>.*?allowForward=1&url=(.*?)&'#先将微博内容全部匹配下来,含url
    sub=r'color:red'#子串
    reg=re.compile(reg)
    reg2=re.compile('<.*?>')#去除其中的<...>
    mats=reg.findall(line)
    if mats!='[]':
        for mat in mats:
            with codecs.open('result.txt','a',encoding='utf-8') as f:#写入utf-8文件
                if mat[0].find(sub)!=-1:#含有子串
                    t=reg2.sub('',mat[0])#剔除其中的<...>
                    f.write(t.decode('unicode_escape').replace('\\','')+'\n')#去除"\"
                    f.write(u'单条微博信息：')
                    f.write(mat[1].replace('\\','')+'\n\n')