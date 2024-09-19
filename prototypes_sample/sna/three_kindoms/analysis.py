#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Description: A tool for analyzing 《水浒传》
Author: Wallace Huang
Date: 2019/6/28
Version: 1.0
"""

import pandas as pd


def read_basic_data(src_file):
    with open(src_file, 'rt') as file:
        data = file.read()
    return data


if __name__ == '__main__':
    novel_data = read_basic_data('./data/shuihuzhuan.csv')
    novel_data = novel_data.replace('\n', '')
    novel_set = novel_data.split(' ')
    novel_set = [k for k in novel_set if k != '']
    # print(novel_set)
    sj_set = [k for k in novel_set if '宋江' in k]

    print('novel length: ', len(novel_set))
    print('song jiang length: ', len(sj_set[0]))
    heros = pd.read_csv('./data/shuihu_heros.csv', header=None, sep=',', encoding='utf-8', low_memory=True)
    heros.sort_values(1, inplace=True)
    print(heros)
    attr = heros[0][0:10]
    print(attr)
    v1 = heros[1][0:10]
    print(v1)

    # plt.bar.add("年收入（万）", attr, v1, is_stack=True, is_label_show=True)
    # plt.bar.render('水泊梁山年收入TOP10.html')
    #
    net_df = pd.DataFrame(columns=['Source', 'Target', 'Weight', 'Source_Ratio', 'Target_Ratio'])
    for i in range(0, 107):
        for j in range(i + 1, 108):
            this_weight = len([k for k in novel_set if heros[0][i] in k and heros[0][j] in k])
            net_df = net_df.append({'Source': heros[0][i], 'Target': heros[0][j], 'Weight': this_weight,
                                    'Source_Ratio': this_weight / heros[1][i],
                                    'Target_Ratio': this_weight / heros[1][j]}, ignore_index=True)
            print(str(i) + ':' + str(j))
