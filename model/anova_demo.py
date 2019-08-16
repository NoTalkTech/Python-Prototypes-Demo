# -*- coding: UTF-8 -*-
"""
Description: 
Author: Wallace Huang
Date: 2019/8/14
Version: 1.0
"""
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kstest
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    current_path = os.getcwd()

    data = [['a1', 25.6], ['a1', 22.2], ['a1', 28.0], ['a1', 29.8], ['a2', 240.4], ['a2', 230.4], ['a2', 210.4]]
    df = pd.DataFrame(data, columns=['A', 'B'])
    print(df)
    model1 = ols('B ~ A', df).fit()
    anova1 = anova_lm(model1)
    print(anova1)

    file = current_path + '/../resources/anova_sample.csv'
    data = pd.read_table(file, sep=',', encoding='utf-8', low_memory=True)
    cols = data.columns.drop('rep').values
    for i in cols:
        try:
            print('Start to analyze {}.'.format(i))
            data_test = data[[i, 'rep']]
            # data_test.dropna(inplace=True)
            # data_test['sorted_index'] = data_test[i].groupby(data_test['rep']).rank()
            # data_test['index'] = data_test.apply(lambda x: int(x['sorted_index'] - 1), axis=1)
            # sort_cols = ['index', 'rep', i]
            # sort_df = data_test.reindex(columns=sort_cols)
            # formula = '{} ~ C(rep)'.format(i)
            # model = ols(formula, sort_df).fit()
            formula = '{} ~ rep'.format(i)
            model = ols(formula, data_test).fit()
            plt.figure()
            model.resid.plot.density()
            # pl.show()
            # plt.show()
            plt.savefig('{}.png'.format(i))
            anova_res = anova_lm(model, typ=2)
            # anova_res = anova_lm(model)
            print('ANOVA : fscore = {}, pvalue = {}'.format(anova_res['F'].get_value(0),
                                                            anova_res['PR(>F)'].get_value(0)))
            kstest_res = kstest(np.array(model.resid).T, 'norm')
            print('Kstest: statistic = {}, pvalue = {}'.format(kstest_res.statistic, kstest_res.pvalue))
            print('Succeed to analyze {}'.format(i))
        except Exception as e:
            print('Failed to analyze {}. Exception: {}'.format(i, e))
