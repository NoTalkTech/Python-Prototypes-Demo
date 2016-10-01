#!/usr/bin/env python
# coding=utf-8

# author chaochao
import os, sys, urllib.request, re, time


# from bs4 import BeautifulSoup

# get html content
def getHtml(url):
    file = urllib.request.urlopen(url)
    html = file.read()
    html = html.decode('utf8')
    return html


# According to the regular matching data    return data list
def getList(html, reg):
    reg = re.compile(reg)
    list = re.findall(reg, html)
    return list


# down pictures
def download(imgList, name, title):
    path = os.getcwd()
    base_floder = path + '/lofter/'
    # filter special character
    title = title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"',
                                                                                                                '').replace(
        '<', '').replace('>', '').replace('|', '')
    curr_floder = base_floder + title

    if not os.path.exists(curr_floder):
        os.makedirs(curr_floder)
    x = 0
    global pass_count
    global total_count
    for imgurl in imgList:
        file_name = name + str(x)
        try:
            # if exists a same pic  pass to save pic and continue download
            if os.path.exists(curr_floder + '/%s.jpg' % file_name):
                pass_count += 1
                total_count += 1
                print('The picture already exists，pass~~~~~~')
                x += 1
                continue
            urllib.request.urlretrieve(imgurl, curr_floder + '/%s.jpg' % file_name)
            total_count += 1
            print('download picture ' + str(x + 1) + ' successed!')
            x += 1
        except:
            x += 1
            continue


def downlofter(start=1, end=80):
    while (start < end):
        url = 'http://sexy.faceks.com/?page=' + str(start)
        try:
            print(url)
            html = getHtml(url)
            print('Get html code successed……')
            reg = r'<a\s+class="img"\s+href="(.+)"'
            urllist = getList(html, reg)

            print('Get URL list successfully! Start loop download……')
        except:
            print('Something wrong! try to get to the next page……')
            start = start + 1
            continue
        index = 0
        for u in urllist:
            print('Start page %s，item %s ……' % (start, index + 1))
            try:
                h = getHtml(u)
                print('Get item html code successed……')
                title_reg = r'<title>(.+)</title>'
                title = getList(h, title_reg)[0]
                img_reg = r'bigimgsrc="(.+?\.jpg)"'
                img_list = getList(h, img_reg)
                print('Parsing HTML succeed！total of %s pictures，begin download……' % len(img_list))
                name = str(start) + str(index)
                download(img_list, name, title)
                index = index + 1
            except:
                print('Something wrong!, try to get to the next item……')
                start = start + 1
                index = index + 1
                continue
        start = start + 1


pass_count = 0
total_count = 0

index = input('please input start page:')
last = input('please input end page:')
start = time.time()
downlofter(int(index), int(last))
end = time.time()
print('==========================Statistics============================')
print('Download ：%s pictures' % total_count)
print('Pass ：%s pictures' % pass_count)
print('Total Time：%s ms' % (end - start))
input("press enter to exit...")
