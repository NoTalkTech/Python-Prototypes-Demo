#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import os
import platform
import sys

from pandas import datetime
from pandas import read_csv


def f_handler(f, mode):
    fo = open(f, mode)
    print "FileName: ", fo.name
    print "Does it opened: ", fo.closed
    print "Access mode: ", fo.mode
    print "SoftSpace: ", fo.softspace
    return fo


def parser(x):
    # print datetime.strptime('1900-01', '%Y-%m')
    return datetime.strptime('190{}'.format(x), '%Y-%m')


def r_file(f):
    # type: (object) -> object
    return read_csv(f, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser, seq=';')


def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler("FileUtils.log")
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    logger.info("Script path: {}".format(cur_file_dir()))

    # 得到当前工作目录,即当前Python脚本工作的目录路径:
    print "The current working directory: {}".format(os.getcwd())
    # 获取系统名称
    print "OS name: {}".format(platform.system())
    # 路径分割符
    print "OS separator: {}".format(os.sep)

    # 返回指定目录下的所有文件和目录名
    filePath = os.getcwd() + os.sep + "resources" + os.sep

    fileName = '{}example_data.csv'.format(filePath)
    print "File Path: {}".format(filePath)
    print "Files List: {}".format(os.listdir(filePath))

    # r+ 以读写模式打开文件,文件可读可写，可写到文件的任何位置
    # w+ 以只写模式打开文件,先把文件内容清空（truncate the file first）
    # a+ 以添加模式打开文件,只能写到文件末尾
    f1 = f_handler(fileName, "a+")
    f2 = f_handler(fileName, "r+")
    f1.close()
    f2.close()

    series = read_csv(fileName, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser, sep=';')
    diff = series.diff()
    print "diff series: {}".format(diff)
    # pyplot.plot(diff)
    # pyplot.show()
    # pyplot.close()
