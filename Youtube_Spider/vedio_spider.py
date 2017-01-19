#!/usr/bin/env python3
# encoding=utf-8
# from importlib import reload
from imp import reload

import requests
import re
import json
import sys
import shutil
import urlparse2

""" youtube """
reload(sys)
sys.getdefaultencoding().encode('utf-8')
res = requests.get('https://www.youtube.com/watch?v=3ZyVeyWV59U')

html = res.text.decode('gbk', 'ignore').encode('utf-8')
m = re.search('"args":({.*?}),', html)
# print m.group(1)
jd = json.loads(m.group(1))
# print jd["url_encoded_fmt_stream_map"]
a = urlparse2.parse_qs(jd["url_encoded_fmt_stream_map"])
print(a['url'][0])
res2 = requests.get(a['url'][0], stream=True)
f = open('youtube.mp4', 'wb')
shutil.copyfileobj(res2.raw, f)
f.close()
