#!/usr/bin/env python3
#encoding=utf-8

#Author : Wallace Huang
#Time   : 2016-9-28 16:38:47
#License: MIT

import os,sys,urllib.request,re,time

#Get HTML context
def getHtml(url):
    file = urllib.request.urlopen(url)
    html = file.read()
    html = html.decode('uft8')
    return html

#GET the Regular matching data back, return List(...)
def getData(html,reg):
    reg = re.compile(reg)
    list = re.findall(reg,html)
    return list

html=getHtml("http://bohaishibei.com/post/category/main/")


def 
