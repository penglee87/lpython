# -*- coding:utf-8 -*-
# pip3 install html5lib
# pip3 install lxml
# http://www.w3school.com.cn/css/css_selector_type.asp
__author__ = 'hunterhug'
from bs4 import BeautifulSoup
soup = BeautifulSoup("<html class='c c1' id='id'>"
                     "<head><title>The Dormouse's story</title><meta charset='utf-8' /></head>"
                     "<p>sdd</p><p>dd\n</p>"
                     "\n"
                     "</html>", "html.parser")
print(type(soup)) # <class 'bs4.BeautifulSoup'>

tag=soup.html
print(tag)            # 得到标记的内容
print(tag.name)     # 标记名称
print(tag.attrs)    # 标记内所有属性值
print(tag['class']) # 标记内某个属性值
# print(tag.get('class'))
print(tag.string)      # 标记内有标记则里面字符串没有

tag1=soup.p
print(type(tag1))              # <class 'bs4.element.Tag'>
print(tag1)                    # 只能得到第一个标记
print(type(tag1.string))     # <class 'bs4.element.NavigableString'>

print('-'*50)
print(tag1.string)  # 得到标记内字符串
print('-'*50)


# xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml')
# print(xml_soup.p['class'])

xml_soup1 = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')
print(xml_soup1.p['class'])


markup = "<b>都是<!--Hey, buddy. Want to buy a used parser?-->都是<!--Hey, buddy. Want to buy a used parser?--></b>"
marksoup = BeautifulSoup(markup,'html.parser')
comment = marksoup.b.string
print(type(comment))     # <class 'bs4.element.Comment'>
print(comment)            # 打印注释内容，多个注释则内容为空
print(marksoup.b)            # 打印整个标记，下面一个标记空一行
print(marksoup.b.prettify())

# 找所有元素
alla = soup.find_all('p')
print(alla)
nodes = soup.contents
print(nodes)
print(nodes[0].name)
nodess=soup.html.contents
print(nodess)
print(len(nodess))

# 子节点循环
for child in soup.html.children:
    print(child)

# 向左深度递归
for child in soup.html.descendants:
    print(child)

print('-'*50)
for string in soup.strings:
    print(repr(string))
print('-'*50)

# 得到父节点
title_tag = soup.title
print(title_tag.parent)
print(title_tag.parent.name)

# 递归父节点
for parent in title_tag.parents:
    if parent is None:
        print(parent,'none')
    else:
        print(parent.name)

print('-'*50)
print(soup.prettify())
print('-'*50)

# 兄弟节点
str = """<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>"""
brother = BeautifulSoup(str, 'html.parser')
link = brother.a
print(link)
print('-'*50)
print(repr(link.next_sibling))
print('-'*50)
print(link.next_sibling) # str()出来的值是给人看的。。。repr()出来的值是给python看的
print(link.next_sibling.next_sibling)
print(link.next_sibling.next_sibling.previous_sibling.previous_sibling)

print('-'*50)
for sibling in link.next_siblings:
    print(repr(sibling))

print('-'*50)
for sibling in brother.find(id="link3").previous_siblings:
    print(repr(sibling))