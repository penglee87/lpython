#!/usr/bin/env python
# coding=utf-8
"""
作者：桥头堡
链接：https://www.zhihu.com/question/19801131/answer/27459821
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

有些库函数（libraryfunction）却要求应用先传给它一个函数，好在合适的时候调用，以完成目标任务。
这个被传入的、后又被调用的函数就称为回调函数（callback function）
"""
#回调函数1
#生成一个2k形式的偶数
def double(x):
    return x * 2
    
#回调函数2
#生成一个4k形式的偶数
def quadruple(x):
    return x * 4



#中间函数(库函数)
#接受一个生成偶数的函数作为参数
#返回一个奇数
def getOddNumber(k, getEvenNumber):
    return 1 + getEvenNumber(k)
    
#起始函数，这里是程序的主函数
def main():    
    k = 1
    #当需要生成一个2k+1形式的奇数时
    i = getOddNumber(k, double)
    print(i)
    #当需要一个4k+1形式的奇数时
    i = getOddNumber(k, quadruple)
    print(i)
    #当需要一个8k+1形式的奇数时
    i = getOddNumber(k, lambda x: x * 8)
    print(i)
    
if __name__ == "__main__":
    main()

