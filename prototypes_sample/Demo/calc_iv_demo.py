#!/usr/bin/python
# -*- coding: UTF-8 -*-
# calc iv demo
import numpy as np
from scipy.stats import stats


def calc_iv_equal_percent(x_col, y_col, k, point):
    a = [0 for i in range(k)]
    for i in range(k):
        assert isinstance(point, int)
        a[i] = stats.scoreatpercentile(x_col, i * point)
    woe = np.zeros(np.unique(a).shape)
    iv = np.zeros(np.unique(a).shape)
    n_1 = np.sum(y_col == 1)
    n_1_group = np.zeros(np.unique(a).shape)
    n_0 = np.sum(y_col == 0)
    n_0_group = np.zeros(np.unique(a).shape)
    for i in range(len(np.unique(a))):
        if i < max(range(len(np.unique(a)) - 1)):
            n_1_group[i] = y_col[(x_col >= a[i]) & (x_col < a[i + 1]) & (y_col == 1)].count
            n_0_group[i] = y_col[(x_col >= a[i]) & (x_col < a[i + 1]) & (y_col == 0)].count
            woe[i] = np.log(((np.sum(n_1_group[i]) / n_1) / (np.sum(n_0_group[i]) / n_0)))
            iv[i] = (np.sum(n_1_group[i]) / n_1 - np.sum(n_0_group[i]) / n_0) * np.log(
                ((np.sum(n_1_group[i]) / n_1) / (np.sum(n_0_group[i]) / n_0)))
        elif i == len(np.unique(a)) - 1:
            n_1_group[i] = y_col[(x_col >= a[i]) & (y_col == 1)].count()
            n_0_group[i] = y_col[(x_col >= a[i]) & (y_col == 0)].count()
            woe[i] = np.log(((np.sum(n_1_group[i]) / n_1) / (np.sum(n_0_group[i]) / n_0)))
            iv[i] = (np.sum(n_1_group[i]) / n_1 - np.sum(n_0_group[i]) / n_0) * np.log(
                ((np.sum(n_1_group[i]) / n_1) / (np.sum(n_0_group[i]) / n_0)))
    s_iv = sum(iv)
    return s_iv, woe
