#!/usr/bin/env python3
# encoding=utf-8
import os
import re
import sys
import threading
import time
from imp import reload

import requests

# from importlib import reload

reload(sys)
sys.getdefaultencoding().encode("gbk")


class Archives(object):
    global start

    @staticmethod
    def save_links(url):

        try:
            data = requests.get(url)
            content = data.text
            link_pat = '"(ed2k://\|file\|[^"]+?\.(S\d+)(E\d+)[^"]+?1024X\d{3}[^"]+?)"'
            name_pat = re.compile(r'<h2 class="entry_title">(.*?)</h2>', re.S)
            links = set(re.findall(link_pat, content))
            name = re.findall(name_pat, content)
            links_dict = {}
            count = len(links)
        except Exception as e:
            print(e)
            pass
        for i in links:
            links_dict[int(i[1][1:3]) * 100 + int(i[2][1:3])] = i  # 把剧集按s和e提取编号

        try:
            with open('./USTVSeries/{0}.txt'.format(name[0].replace('/', ' ')), 'w') as f:
                print(name[0])
                for i in sorted(list(links_dict.keys())):  # 按季数+集数排序顺序写入
                    f.write(links_dict[i][0] + '\n')
                    f.flush()
            print("Get links ... ", name[0], count)
        except Exception as e:
            print(e)
            pass

    def get_urls(self):
        try:
            for i in range(2015, 25000):
                base_url = 'http://cn163.net/archives/'
                url = base_url + str(i) + '/'
                if requests.get(url).status_code == 404:
                    print(repr(url + ": Return 404 code."))
                    continue
                else:
                    print(repr(url + ": Successfully."))
                    self.save_links(url)
        except Exception as e:
            print(e)
            pass

    def main(self):
        thread1 = threading.Thread(target=self.get_urls())
        thread1.start()
        thread1.join()


def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


if __name__ == '__main__':
    start = time.time()
    print(repr(start))
    a = Archives()
    a.main()
    end = time.time()
    print(repr(end - start))
