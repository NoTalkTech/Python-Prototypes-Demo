#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
from statsmodels.compat import lrange
from statsmodels.tsa.stattools import acf, acovf

if __name__ == '__main__':
    # a = np.arange(1, 16).T.reshape((5, 3))
    # print a

    b = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    x = np.asarray(b)
    print "Input Array: x = ", x
    nobs = x.shape[0]  # 获取矩阵的行数。即第一维度
    print "Array rows: Nobs = ", nobs

    lags = 1
    if lags is None:
        lags = lrange(1, 41)  # TODO: check default; SS: changed to 40
    elif isinstance(lags, (int, long)):
        lags = lrange(1, lags + 1)
    maxlag = max(lags)
    lags = np.asarray(lags)

    acfx = acf(x, nlags=maxlag)  # normalize by nobs not (nobs-nlags)
    acovf
    # # SS: unbiased=False is default now
    # #    acf2norm = acfx[1:maxlag+1]**2 / (nobs - np.arange(1,maxlag+1))
    # acf2norm = acfx[1:maxlag + 1] ** 2 / (nobs - np.arange(1, maxlag + 1))
    #
    # qljungbox = nobs * (nobs + 2) * np.cumsum(acf2norm)[lags - 1]
    # pval = stats.chi2.sf(qljungbox, lags)
    # if not boxpierce:
    #     return qljungbox, pval
    # else:
    #     qboxpierce = nobs * np.cumsum(acfx[1:maxlag + 1] ** 2)[lags - 1]
    #     pvalbp = stats.chi2.sf(qboxpierce, lags)
    #     return qljungbox, pval, qboxpierce, pvalbp
    #


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
