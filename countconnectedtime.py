#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib2
import sqlite3

isconnected = False
starttime = endtime = None


def insert_data(xcurs, start_time, end_time, total_time):
    query = 'INSERT INTO time(id, starttime, endtime,  totaltime) \
             VALUES (%s, %s, %s, %s)' % (
             start_time, start_time, end_time, total_time)
    xcurs.execute(query) # 执行 SQL 语句


url = 'http://www.baidu.com/favicon.ico'
# 模拟浏览器
user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) \
                            Gecko/20100101 Firefox/4.0.1'
headers = { 'User-Agent' : user_agent }
request = urllib2.Request(url=url, headers=headers)

conn = sqlite3.connect('totals.db')  # 连接数据库
curs = conn.cursor()  # 获取游标
sleep_time = 60 #每次循环的间隔(秒)
counts = 0

while True:
    print 'start'
    try:
        u = urllib2.urlopen(request)
    except:
        print 'error'
        print isconnected
        if isconnected: # 连接第一次断开
            endtime = time.time()
            print endtime
            totaltime = (endtime - starttime + 
                                    sleep_time * counts)/60.0 #以1分钟为单位计时
            if totaltime%1 > 0:
                totaltime = int(totaltime) + 1
            print totaltime
            # 写入文件/数据库
            # write(starttime, endtime, totaltime) # 结果舍弃秒数，秒入为分
            starttime = time.strftime('%Y/%m/%d %H:%M',
                                time.localtime(starttime)) #格式化日期
            endtime = time.strftime('%Y/%m/%d %H:%M',
                                time.localtime(endtime)) # 格式化日期
            print starttime
            print endtime
            try:
                insert_data(curs, starttime, endtime, totaltime)
            except Exception, e:
                print e
            #except:
                # 建表
                curs.execute('''
                CREATE TABLE time (
                        id                TEXT        PRIMARY KEY,
                        starttime         FLOAT,
                        endtime          FLOAT,
                        totaltime       FLOAT
                )
                ''')
                
                insert_data(curs, starttime, endtime, totaltime)
            conn.commit()  # 提交数据
            # pass
            isconnected = False # 标记连接状态为断开
    else:
        print 'ok'
        if not isconnected: # 第一次连接
            starttime = time.time()
            print starttime
            isconnected = True
            print isconnected
            counts = 0
            # pass
    print 'end'
    time.sleep(sleep_time) # 每过一段时间(秒)循环一次
    counts += 1

conn.close()