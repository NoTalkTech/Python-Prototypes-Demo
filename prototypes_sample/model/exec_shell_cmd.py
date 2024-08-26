# -*- coding: UTF-8 -*-
"""
Description: A tool for executing shell command
Author: Wallace Huang
Date: 2019/6/28
Version: 1.0
"""

import subprocess

if __name__ == '__main__':
    cmd = ['ls', '-lha']
    print('\n---------- call() method ----------')
    subprocess.call(cmd, shell=False)
    print('\n---------- run() method ----------')
    s_proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=False,
                            universal_newlines=True)
    print(s_proc.stdout)
    print('return_code => ', s_proc.returncode)
    print('\n---------- Popen() method ----------')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    print(output)
    print(errors)
