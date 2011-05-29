#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib2

isconnected = False
starttime = endtime = None

url = 'www.baidu.com/favicon.ico'
# 模拟浏览器
user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) \
                            Gecko/20100101 Firefox/4.0.1'
headers = { 'User-Agent' : user_agent }
request = urllib2.Request(url=url, headers=headers)

while True:
    print 'start'
    try:
        urllib2.open(request)
    except:
        if isconnected:
            #endtime = time.time()
            # counttime = (endtime-starttime)/60.0
            # if counttime%1 > 0:
            #        counttime = int(counttime) + 1
            # 写入文件/数据库
            # write(starttime, endtime, counttime) # 结果舍弃秒数，秒入为分
            pass
        isconnected = False
    else:
         if not isconneceted:
            #starttime = time.time()
            #isconneceted = True
            pass
    print 'end'
    time.sleep(60) # 每一分钟循环一次
