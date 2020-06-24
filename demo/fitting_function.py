#!/usr/bin/python3
#coding:utf-8
 
import numpy as np
from scipy.optimize import leastsq
import pylab as pl
import math
 
#定义函数
#y= a*ln(x)+b
 
def func(x,p):
   A,B=p
   return A*np.log(x)+B
 
 
#定义残差函数
def residuals(p,y,x):
   ret=y-func(x,p)
   return ret
 

if __name__ == "__main__":
    x3 = np.linspace(0, 30, 1000)  # 用于画图精度的调节
    x0 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # x变量, 在这里2,3,7全部减1
    x2 = np.array(x0)  # 向量化x变量
    y0 = [0.64, 0.60, 0.58, 0.56, 0.56, 0.55,
        0.54, 0.52, 0.52, 0.50, 0.50, 0.50]  # y
    y2 = np.array(y0)  # 向量化
    p0 = [0.5, 0.5]  # 取值起始点
    
    qs = leastsq(residuals, p0, args=(y2, x2))  # 最小二乘法
    print(qs[0])  # 为最佳的拟合函数参数
    pl.plot(x0, y0, label='Real', color='red')  # 画出实际图像
    pl.plot(x3, func(x3, qs[0]), label='sim', color='blue')  # 预测图像
