#!/usr/bin/python
# -*- coding: UTF-8 -*-
# python demo
import os
import pandas as pd
from os.path import join


def lookup_target_func1(arr, tgt):
    # O(n ^ 2)
    nums_len = len(arr)
    for i in range(0, nums_len):
        for j in range(i + 1, nums_len):
            if arr[i] + arr[j] == tgt:
                return [i, j]


def lookup_target_func2(arr, tgt):
    # O(n)
    seen_dict = {}
    for i, num in enumerate(arr):
        search = tgt - num
        if search in seen_dict:
            return [seen_dict[search], i]
        else:
            seen_dict[num] = i


def lookup_target_func3(arr, tgt):
    # O(nlogn)
    global v_left, v_right, two_sum
    sorted_arr = sorted(arr)
    left, right = 0, len(arr) - 1

    while left < right:
        v_left, v_right = sorted_arr[left], sorted_arr[right]
        two_sum = v_left + v_right

        if two_sum > tgt:
            right -= 1
        elif two_sum < tgt:
            left += 1
        else:  # 找到了
            left_index = arr.index(v_left)
            # 如果值相同就查找下一个该值的索引
            right_index = arr.index(v_right, left + 1) \
                if v_right == v_left else arr.index(v_right)
            return [left_index, right_index]


if __name__ == '__main__':
    # array process
    nums = [2, 7, 11, 15]
    target = 26
    print(lookup_target_func1(nums, target))
    print(lookup_target_func2(nums, target))
    print(lookup_target_func3(nums, target))

    # Read parquet file
    current_path = os.getcwd()
    print('=> current_path = {}'.format(current_path))
    data1 = pd.read_parquet(
        join(current_path, 'hdfs/part-00002-140b6595-b507-4aca-afd9-a147ce98ffd4-c000.snappy.parquet'),
        engine='pyarrow')
    print('=> data_shape = {}'.format(data1.shape))
    print('=> data_iloc {}'.format(data1.iloc[0:20, :]))

    # print(data2)
    # data = pd.concat([data1, data2, data3], axis=0, ignore_index=True)
    # print(data)
