#coding=utf-8
__author__ = 'Hsars'
import urllib2, time, datetime
from lxml import etree
import sqlite3,time

user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
header = {"User-Agent": user_agent}
nn_url = "http://tvp.daxiangdaili.com/ip/?tid=556615738536308&filter=on&num=5&ports=80,8080,3128"
req = urllib2.Request(nn_url, headers=header)
resp = urllib2.urlopen(req, timeout=5)
content = resp.read()
line  = content.split("\r\n")
print line


