# -*- coding:utf-8 -*-
from imp import reload

import requests
import re
import sys
import threading
import time

reload(sys)
sys.getfilesystemencoding()


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
            pass
        for i in links:
            links_dict[int(i[1][1:3]) * 100 + int(i[2][1:3])] = i  # 把剧集按s和e提取编号

    def get_urls(self):
        try:
            for i in range(2015, 25000):
                base_url = 'http://cn163.net/archives/'
                url = base_url + str(i) + '/'
                if requests.get(url).status_code == 404:
                    continue
                else:
                    self.save_links(url)
        except Exception as e:
            pass

    def main(self):
        thread1 = threading.Thread(target=self.get_urls())
        thread1.start()
        thread1.join()

if __name__ == '__main__':
    start = time.time()
    a = Archives()
    a.main()
    end = time.time()
    print(end - start)
