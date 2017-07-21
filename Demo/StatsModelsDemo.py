#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller as ADF


def statsTest(x, lags=1):
    """

    :param x:
    :type lags: int
    """
    print "x: {}".format(x)
    inSer = pd.Series(x)
    print "inSer: {}".format(inSer)
    adf = ADF(inSer, maxlag=lags)
    print "adf: {}".format(adf[1])
    [_, [lb]] = acorr_ljungbox(inSer, lags=lags)
    print "lb: {}".format(lb)


if __name__ == '__main__':
    x = [2.4691546819860264, 4.60288091695595, 0.15927628269880256, 8.286730570556205, 3.5709442862476024,
         0.43502622854919126, 4.1084893867934005]

    res = np.polyval(x, -2.117294094017699)
    print "res: {}".format(res)

    statsTest(x)
