# -*- coding: UTF-8 -*-
"""
Description: matplotlib.pyplot demo
Author: Wallace Huang
Date: 2019/10/16
Version: 1.0
"""
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    max_x = 2 * np.pi
    x = np.linspace(-max_x, max_x)
    y1 = np.sin(x)
    y2 = np.cos(x)
    # y3 = np.tan(x)
    plt.figure(figsize=[8, 5])
    plt.title('Compare cosx with sinx')
    plt.plot(x, y1, 'r--', label='sin(x)')
    plt.plot(x, y2, 'b--', label='cos(x)')
    # plt.plot(x, y3, 'k--', label='tan(x)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    # plt.axis([0, 2 * np.pi, -1, 1])  # 设置坐标范围axis([xmin,xmax,ymin,ymax])
    plt.legend()
    plt.show()
