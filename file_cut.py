#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 实现文件切割
"""

with open('filename.csv') as f:
    ls = f.readlines()
    total = len(ls)
    per_page = 10000
    
    for i in range(1,total/per_page+2):
        lines = ls[(i-1)*per_page:i*per_page]
        with open('filename_{0}.csv'.format(i),'w') as fi:
            fi.writelines(lines)