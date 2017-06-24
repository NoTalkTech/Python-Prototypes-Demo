#!/usr/bin/python
# -*- coding: UTF-8 -*-

print "你好，世界"

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


list = [ 'runoob', 786 , 2.23, 'john', 70.2 ]
tinylist = [123, 'john']

print list               # 输出完整列表
print list[0]            # 输出列表的第一个元素
print list[1:3]          # 输出第二个至第三个的元素
print list[2:]           # 输出从第三个开始至列表末尾的所有元素
print tinylist * 2       # 输出列表两次
print list + tinylist    # 打印组合的列表