#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os


class FileUtils:
    __fileName = None
    __document = None
    __filepath = None

    @classmethod
    def loginfo(cls, msg):
        print(repr(msg))

    def __init__(self, filepath=os.getcwd(), filename=''):
        # 构造函数，生成对像时被调用
        print("Start to init object FileUtils")
        self.__fileName = filename
        self.__filepath = filepath
        if self.__filepath.endswith(os.sep):
            self.__document = open(filepath + filename, "w+")
        else:
            self.__document = open(filepath + os.sep + filename, "w+")
        print("Succeed to init object FileUtils")

    def __del__(self):
        # 析构函数，删除对像时被调用
        print("Start to delete object FileUtils")
        self.__document.close()
        print("Succeed to delete object FileUtils")

    def get_file_name(self):
        # type: () -> str
        return "文件名: {}".format(self.__document.name)

    def read_context(self):
        self.__document.write("Test File\nwelcome!")
        # 输出当前指针位置
        print(self.__document.tell())
        # 设置指针回到文件最初
        self.__document.seek(os.SEEK_SET)
        context = self.__document.read()
        return context


if __name__ == '__main__':
    print(os.getcwd())
    handler = FileUtils(os.getcwd(), "shuihuzhuan.csv")
    FileUtils.loginfo(handler.__doc__)
    FileUtils.loginfo(handler.get_file_name())
    FileUtils.loginfo(handler.read_context())
