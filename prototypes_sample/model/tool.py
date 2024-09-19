#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
Description:
Author: Wallace Huang
Date: 2019-06-27
Version: 1.0
"""

import numpy as np
from scipy.stats import kstest, normaltest

if __name__ == '__main__':
    x = np.linspace(-15, 15, 9)
    # kstest 正态性检验
    print(kstest(x, 'norm'))

    # normaltest
    y = np.random.randn(10, 20)
    print(y)
    print(normaltest(y, axis=None))
