#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
Description: A tool for calculating the difference between TP / (TP + FP) and FN / (FN + TN)
Author: wallace
Date: 2019/6/27
Version: 1.0
"""

import argparse
import os

import pandas as pd
import pandas.core.common as com


def calc_diff(file, label_field, predict_field, sep=',', encoding='utf-8', ignore_fields=None, split_rate=0.7):
    if not os.access(file, os.F_OK):
        print('FileNotFoundError: %s not found' % file)
        exit(-1)
    else:
        df = pd.read_csv(file, sep=sep, encoding=encoding, low_memory=True)
        for field in [predict_field, label_field]:
            if field not in df.columns:
                print('KeyWordError: %s not found' % field)
                exit(-1)

        df.sort_values(predict_field, ascending=False, inplace=True)
        label = df[label_field].values.astype(float)

        if not ignore_fields:
            pass
        else:
            print('ignore_fields: ', ignore_fields)
            df.drop(com.maybe_make_list(ignore_fields), axis=1, inplace=True, errors='ignore')

        total_num = len(label)
        split_position = int(total_num * split_rate)
        tp_rate = sum(label[0: split_position]) * 1.0 / split_position
        fn_rate = sum(label[split_position:]) * 1.0 / (total_num - split_position)
        diff = tp_rate - fn_rate
        print('split_rate: %f, tp_rate: %f, fn_rate: %f, diff: %f' % (
            split_position * 1.0 / total_num, tp_rate, fn_rate, diff))
        exit(0)


def str_2_list(s, sep=','):
    if s is None or len(s.strip()) == 0:
        return []
    else:
        return list(map(lambda x: x.strip(), s.strip().split(sep)))


if __name__ == '__main__':
    """
    USAGE: calc_diff.py --src_file source.csv --predict predict_col --label label_col --ignore_fields col0,col1
    """
    parse = argparse.ArgumentParser()
    parse.add_argument('--src_file', type=str, default=None)
    parse.add_argument('--predict', type=str, default='predict')
    parse.add_argument('--label', type=str, default='label')
    parse.add_argument('--ignore_fields', type=str, default='')
    arg = parse.parse_args()
    calc_diff(arg.src_file, arg.label, arg.predict, ignore_fields=str_2_list(arg.ignore_fields))
