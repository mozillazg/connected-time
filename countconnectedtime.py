#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib2
import sqlite3

isconnected = False
starttime = endtime = None


def insert_data(xcurs, start_time, end_time, count_time):
    query = 'INSERT INTO time(id, starttime, endtime,  counttime) \
             VALUES (%s, %s, %s, %s)' % (
             start_time, start_time, end_time, count_time)
    xcurs.execute(query) # 执行 SQL 语句


url = 'http://www.baidu.com/favicon.ico'
# 模拟浏览器
user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) \
                            Gecko/20100101 Firefox/4.0.1'
headers = { 'User-Agent' : user_agent }
request = urllib2.Request(url=url, headers=headers)

conn = sqlite3.connect('counts.db')  # 连接数据库
curs = conn.cursor()  # 获取游标
sleep_time = 60 #每次循环的间隔(秒)

while True:
    print 'start'
    try:
        u = urllib2.urlopen(url)
    except:
        print 'error'
        print isconnected
        if isconnected: # 连接第一次断开
            endtime = time.time()
            print endtime
            counttime = (endtime - starttime + sleep_time)/60.0 #以1分钟为单位计时
            if counttime%1 > 0:
                counttime = int(counttime) + 1
            print counttime
            # 写入文件/数据库
            # write(starttime, endtime, counttime) # 结果舍弃秒数，秒入为分
            try:
                insert_data(curs, starttime, endtime, counttime)
            except Exception, e:
                print e
            #except:
                # 建表
                curs.execute('''
                CREATE TABLE time (
                        id                TEXT        PRIMARY KEY,
                        starttime         FLOAT,
                        endtime          FLOAT,
                        counttime       FLOAT
                )
                ''')
                
                insert_data(curs, starttime, endtime, counttime)
            conn.commit()  # 提交数据
            # pass
            isconnected = False # 标记连接状态为断开
    else:
        print 'ok'
        if not isconnected:
            starttime = time.time()
            print starttime
            isconnected = True
            print isconnected
            # pass
    print 'end'
    time.sleep(sleep_time) # 每过一段时间(秒)循环一次


conn.close()