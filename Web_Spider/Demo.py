#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time

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
    for value in vartuple:
        print value
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

# 循环语句
fruits = ['banana', 'apple', 'mango']
for index in range(len(fruits)):
    print '当前水果 :', fruits[index]

for num in range(10, 20):  # 迭代 10 到 20 之间的数字
    for i in range(2, num):  # 根据因子迭代
        if num % i == 0:  # 确定第一个因子
            j = num / i  # 计算第二个因子
            print '%d 等于 %d * %d' % (num, i, j)
            break  # 跳出当前循环
    else:  # 循环的 else 部分
        print num, '是一个质数'

prime = []  # 输出 2 到 100 简的质数
for num in range(2, 100):  # 迭代 2 到 100 之间的数字
    for i in range(2, num):  # 根据因子迭代
        if num % i == 0:  # 确定第一个因子
            break  # 跳出当前循环
    else:  # 循环的 else 部分
        prime.append(num)
print prime

rows = int(raw_input('输入行数：'))  # 打印空心等边三角形
for i in range(0, rows):
    for k in range(0, 2 * rows - 1):
        if (i != rows - 1) and (k == rows - i - 1 or k == rows + i - 1):
            print " * ",
        elif i == rows - 1:
            if k % 2 == 0:
                print " * ",
            else:
                print "   ",
        else:
            print "   ",
    print "\n"

i = 1  # *字塔
while i <= 9:
    if i <= 5:
        print ("*" * i)

    elif i <= 9:
        j = i - 2 * (i - 5)
        print("*" * j)
    i += 1
else:
    print("")

# break语句
for letter in 'Python':  # 第一个实例
    if letter == 'h':
        break
    print '当期字母 :', letter
var = 10  # 第二个实例
while var > 0:
    print '当期变量值 :', var
    var = var - 1
    if var == 5:  # 当变量 var 等于 5 时退出循环
        break

# continue语句
for letter in 'Python':  # 第一个实例
    if letter == 'h':
        continue
    print '当前字母 :', letter

# 字典
people = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
print "dict['Name']: ", people['Name']
print "dict['Age']: ", people['Age']

# time模块
ticks = time.time()
print "当前时间戳为:", ticks
