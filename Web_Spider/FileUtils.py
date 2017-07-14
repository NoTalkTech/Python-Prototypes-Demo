#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pandas import datetime
from pandas import read_csv


def f_handler(f):
    f_Obj = open(f, "wb")
    return f_Obj


def parser(x):
    return datetime.strptime('190' + x, '%Y-%m')


def r_file(f):
    # type: (object) -> object
    return read_csv(f, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)


if __name__ == '__main__':
    # series = r_file("F:\Code\10192057\Code\Web_Spider\example_data.csv\example_data.csv")
    # pyplot.show()
    str = raw_input("Please input: ")
    print str
    fo = f_handler("example_data.csv")
    print "FileName: ", fo.name
    print "Does it opened: ", fo.closed
    print "Access mode: ", fo.mode
    print "Space: ", fo.softspace
