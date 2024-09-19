#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np

if __name__ == '__main__':
    # a = np.arange(1, 16).T.reshape((5, 3))
    # print a

    b = [[1.0, 2.0], [2.0, 1.8], [3.0, 8.0], [4.0, 1.3], [5.0, 4.5], [6.0, 9.2]]
    x = np.asarray(b)
    print("Input Array [x]: ", x)
    rows = x.shape[0]  # 获取矩阵的行数,即第一维度
    print("x_rows: {}".format(rows))

    columns = x.shape[1]  # 获取矩阵的列数,即第二维度
    print("x_cols: {}".format(columns))

    y = x.reshape(3, 4)  # 改变矩阵的维度：行 * 列
    print("New Array [y]: ", y)

    [y_rows, y_cols] = y.shape
    print("y_rows: {}, y_cols: {}".format(y_rows, y_cols))

    # 标准正态分布
    # mu, sigma = 0, 0.1
    # s = np.random.normal(loc=mu, scale=sigma, size=1000)  # loc 均值,scale 标准差,size大小.
    # s_1 = st.norm(mu, sigma).rvs(1000)
    #
    # print abs(mu < np.mean(s)) < 0.01
    # print abs(sigma - np.std(s, ddof=1)) < 0.01
    #
    # count, bins, _ = plt.hist(s, 30, normed=True)
    # plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (bins - mu) ** 2 / (2 * sigma ** 2)), linewidth=2,
    #          color='r')
    # plt.show()
    #
    # ascent = misc.ascent()
    # fig = plt.figure()
    # plt.gray()  # show the filtered result in grayscale
    # ax1 = fig.add_subplot(121)  # left side
    # ax2 = fig.add_subplot(122)  # right side
    #
    # result = ndimage.gaussian_laplace(ascent, sigma=1)
    # ax1.imshow(result)
    #
    # result = ndimage.gaussian_laplace(ascent, sigma=3)
    # ax2.imshow(result)
    # plt.show()
