#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib2
import sqlite3

# 记录上网时长，并将数据写入到数据库

# 插入数据
def insert_data(xcurs, start_time, end_time, total_time):
    sql = 'INSERT INTO time VALUES (?, ?, ?, ?)'
    values = (start_time, start_time, end_time, total_time)
    xcurs.execute(sql, values) # 执行 SQL 语句

# 查询总上网时长
def query_sum(xcurs):
    xcurs.execute('select sum(totaltime) as total from time')
    total = cur.fetchone()['total']# 获取'total'的值
    return total

url = 'http://www.baidu.com/favicon.ico'
# 模拟浏览器
user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) \
                            Gecko/20100101 Firefox/4.0.1'
headers = { 'User-Agent' : user_agent }
request = urllib2.Request(url=url, headers=headers)
# TODO 一个文件夹(如果不存在则创建)保存数据库文件
# 每个月一个数据库(e.g. 2011_05.db)
dbfile = time.strftime('%Y_%m',time.localtime()) + '.db' 
conn = sqlite3.connect(dbfile)  # 连接数据库
curs = conn.cursor()  # 获取游标
isconnected = False  # 网络连接状态
starttime = endtime = None
sleep_time = 6 # 每次循环的间隔(秒)
counts = 0

while True:
    print 'start'
    try:
        urllib2.urlopen(request)
    except:
        print 'error'
        print isconnected
        if isconnected: # 连接第一次断开
            endtime = time.time()
            print endtime
            totaltime = (endtime - starttime)/60.0 #以1分钟为单位计时
            if totaltime%1 > 0:
                totaltime = int(totaltime) + 1 # 结果舍弃秒数，秒入为分
            print totaltime
            starttime = time.strftime('%Y/%m/%d %H:%M:%S',
                                time.localtime(starttime)) #格式化日期
            endtime = time.strftime('%Y/%m/%d %H:%M:%S',
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
                total_month = query_sum(xcurs)
                conn.commit()  # 提交数据
                print '当月总上网时间：' , total_month
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