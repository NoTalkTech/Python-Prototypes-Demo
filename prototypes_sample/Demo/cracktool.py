#!/usr/bin/python
# -*- coding: UTF-8 -*-
# crack tool

import os
import shutil
from time import sleep


def copy_tree(src_path, target_path):
    context = os.listdir(src_path)
    print "Current Files or dirs: ", context
    while True:
        new_context = os.listdir(src_path)
        if new_context != context:
            break
        print "Sleeping for 3 s"
        sleep(3)

    x = [item for item in new_context if item not in context]
    print x
    shutil.copytree(os.path.join(usb_path, x[0]), target_path)


if __name__ == '__main__':
    usb_path = "/Volumes/"
    tgt_path = '/Users/wallace/usb_copy'
    copy_tree(usb_path, tgt_path)
