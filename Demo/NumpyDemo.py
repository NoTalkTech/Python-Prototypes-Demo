#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

if __name__ == '__main__':
    a = np.arange(1, 16).T.reshape((5, 3))
    print a

    # 标准正态分布
    mu, sigma = 0, 0.1
    s = np.random.normal(loc=mu, scale=sigma, size=1000)  # loc 均值,scale 标准差,size大小.
    s_1 = st.norm(mu, sigma).rvs(1000)

    print abs(mu < np.mean(s)) < 0.01
    print abs(sigma - np.std(s, ddof=1)) < 0.01

    count, bins, _ = plt.hist(s, 30, normed=True)
    plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (bins - mu) ** 2 / (2 * sigma ** 2)), linewidth=2,
             color='r')
    plt.show()
