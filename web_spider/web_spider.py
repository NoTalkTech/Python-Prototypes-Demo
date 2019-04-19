#!/usr/bin/env python3
# encoding=utf-8
# Author : Wallace Huang
# Time   : 2016-9-28 16:38:47
import re
import urllib2


# Get HTML context
def gethtml(url):
    print "Request url is: {}".format(url)
    url_req = urllib2.Request(url)
    print "url_req: {}".format(url_req)
    url_file = urllib2.urlopen(url_req)
    url_html = url_file.read()
    url_html = url_html.decode('utf8')
    return url_html


# GET the Regular matching data back, return List(...)
def getdata(htmlcontext, reg):
    reg = re.compile(reg)
    data_ls = re.findall(reg, htmlcontext)
    return data_ls


if __name__ == '__main__':
    keyword = raw_input("Please input a key word: ")
    url1 = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(keyword)
    # url_param = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + keyword
    mailpattern = re.compile("[^\._:>\\-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+")
    imgPattren = re.compile("<img class=*？ src=\"*.jpg\"?")
    html = gethtml(url1)
    # res=getData(html,imgPattren)
    # print repr(html)
    print html
