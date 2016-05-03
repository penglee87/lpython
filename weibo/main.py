#!/usr/bin/env python
#-*-coding:utf-8-*-
 
from WeiboLogin import WeiboLogin
import re
import urllib2
import Matcher
 
def main():
    urlheader='http://s.weibo.com/weibo/'
    para=raw_input('请输入搜索内容：\n')
    page=1
    userlists=open('userlists').readlines()
    reg1=re.compile(r'\\u4f60\\u7684\\u884c\\u4e3a\\u6709\\u4e9b\\u5f02\\u5e38\\uff0c\\u8bf7\\u8f93\\u5165\\u9a8c\\u8bc1\\u7801\\uff1a')    #你的行为有些异常，请输入验证码
    reg2=re.compile(r'\\u62b1\\u6b49\\uff0c\\u672a\\u627e\\u5230')#抱歉，未找到搜索结果
    for userlist in userlists:
        username=userlist.split()[0]
        password=userlist.split()[1]
        weibologin=WeiboLogin(username,password)
        if weibologin.Login()==True:
            print '登录成功'
            user=True    #帐号可用
        while page<=50 and user:
            url=urlheader+para+'&page='+str(page)
            print '获取第%d页。。' % page
            f=urllib2.urlopen(url)
            ###开始匹配网页内容###
            for line in f:
                if re.search(r'pid":"pl_weibo_direct"',line):    #匹配一定要准确！！
                    if reg2.search(line):
                        print '抱歉，未找到结果。。。'
                        return
                    else:    
                        Matcher.matcher(line)
                        page+=1
                        break
                if re.search(r'pid":"pl_common_sassfilter',line):
                    if reg1.search(line):
                        print '此帐号被锁，使用下一个帐号'
                        user=False    #帐号不可用
 
if __name__=='__main__':
    main()