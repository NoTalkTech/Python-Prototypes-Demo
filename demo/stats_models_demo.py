#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller as ADF


def statsTest(x, lags=1):
    """

    :param x:
    :type lags: int
    """
    print("inSer: {}".format(x))
    inSer = pd.Series(x)
    print("inSer_Size: {}".format(inSer.size))
    adf = ADF(inSer, maxlag=lags)
    print("adfStat: {}, p_value: {}".format(adf[0], adf[1]))
    [[lbStat], [lb]] = acorr_ljungbox(inSer, lags=lags)
    print("lbStat: {}, p_value: {}".format(lbStat, lb))


if __name__ == '__main__':
    # x = [0.16343636581778387,0.8238172114549427,2.1763732232699007,3.1157806169329434,5.481172186915939,-0.5758157402636407,7.36018163444155,2.6556312797529555,-5.656031781298027,8.39784850498074,0.4953024240731402,3.9731234329593432,5.429705286387275,-5.500200183832782,8.903813268348173,18.255509059366624,6.085407402594989,13.418560194175567,18.81534320619912,-1.466789962844123,1.6948655798584848,3.7980441980279043,-7.6317946945762705,-6.564264227091046,-35.90116275624339,9.233110175693499]
    # res = np.polyval(x, -2.117294094017699)
    # print "res: {}".format(res)
    x = [1, 2, 3, 6, 7, 3, 1, 4, 6, 89, 5, 7, 2, 1, 20, 60, 1000, 10, 3, 4, 6, 8, 9, 12, 56, 11, 9, 54]
    # y = [1, 2, 3, 4, 5, 6, 7]
    statsTest(x)
    # print "just do a test"
