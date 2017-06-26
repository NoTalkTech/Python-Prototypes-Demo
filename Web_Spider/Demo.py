#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

from Web_Spider.support import print_func

print_func("Runoob")
print_func("Wallace")


if True:
    print "Answer"
    print "True"
else:
    print "Answer"
    print "False"

counter = 100  # 赋值整型变量
miles = 1000.0  # 浮点型
name = "John"  # 字符串

print "Counter: " + str(counter)
print "Miles: " + str(miles)
print "Name: " + name

list = ['runoob', 786, 2.23, 'john', 70.2]
tinylist = [123, 'john']

print list  # 输出完整列表
print list[0]  # 输出列表的第一个元素
print list[1:3]  # 输出第二个至第三个的元素
print list[2:]  # 输出从第三个开始至列表末尾的所有元素
print tinylist * 2  # 输出列表两次
print list + tinylist  # 打印组合的列表

a = 21
b = 10
c = 0

c = a + b
print "1 - c 的值为：", c

c = a - b
print "2 - c 的值为：", c

c = a * b
print "3 - c 的值为：", c

c = a / b
print "4 - c 的值为：", c

c = a % b
print "5 - c 的值为：", c

# 修改变量 a 、b 、c
a = 2
b = 3
c = a ** b
print "6 - c 的值为：", c

a = 10
b = 5
c = a // b
print "7 - c 的值为：", c

flag = False
name = 'luren'
if name == 'python':  # 判断变量否为'python'
    flag = True  # 条件成立时设置标志为真
    print 'welcome boss'  # 并输出欢迎信息
else:
    print name  # 条件不成立时输出变量名称

num = 5
if num == 3:  # 判断num的值
    print 'boss'
elif num == 2:
    print 'user'
elif num == 1:
    print 'worker'
elif num < 0:  # 值小于零时输出
    print 'error'
else:
    print 'roadman'  # 条件均不成立时输出


def printme(str):
    "打印传入的字符串到标准显示设备上"
    print str
    return


printme("Wallace Huang")


# sometime: '2017-06-23 10:30:00' ''
def str2time(sometime):
    # type: (String) -> String
    if len(sometime) == 16:
        stdtime = time.mktime(time.strptime(sometime, "%Y-%m-%d %H:%M"))
    elif len(sometime) == 19:
        stdtime = time.mktime(time.strptime(sometime, "%Y-%m-%d %H:%M:%S"))
    else:
        stdtime = ''
        print 'attention str2time,no time available!'
    return stdtime


printme(str2time('2017-06-23 10:30:00'))


# 不定长参数
def printinfo(arg1, *vartuple):
    # "打印任何传入的参数"
    print "输出: "
    print arg1
    for var in vartuple:
        print var
    return


printinfo(10)
printinfo(70, 60, 50)


def reverse(li):
    for i in range(0, len(li) / 2):
        temp = li[i]
        li[i] = li[-i - 1]
        li[-i - 1] = temp


l = [1, 2, 3, 4, 5]
reverse(l)
print l

# 模块的引入
# import support
# support.print_func("Runoob")

# from support import print_func
# print_func("Runoob")
