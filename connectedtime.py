#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib2
import ConfigParser
import sqlite3

# 记录上网时长，并将数据写入到数据库

# 插入数据
def insert_data(cur, start_time, end_time, total_time):
    sql = 'INSERT INTO time(starttime, endtime, totaltime) VALUES (?, ?, ?)'
    values = (start_time, end_time, total_time)
    cur.execute(sql, values) # 执行 SQL 语句

# 更新数据
def update_data(cur, start_time, end_time, total_time):
    sql = 'update time set endtime=?, totaltime=? where starttime=?'
    values = (end_time, total_time, start_time)
    cur.execute(sql, values)

# 查询总上网时长
def query_sum(cur):
    cur.execute('select sum(totaltime) as total from time')
    total = cur.fetchone()[0] # 获取单一结果集
    return total

# 设置默认配置
def default_config( configs, configfile):
    configs.add_section('General')
    configs.set('General', 'URL', 'http://www.baidu.com/favicon.ico')
    with open(configfile, 'wb') as config_file:
        configs.write(config_file)
        config_file.close()

def total(start, end):
    totaltime = (end - start)/60.0 #以1分钟为单位计时
    if totaltime%1 > 0:
        totaltime = int(totaltime) + 1 # 结果舍弃秒数，秒入为分
    return totaltime

def main():

    CONFIGFILE = 'config.ini'  # 配置文件名称
    config = ConfigParser.RawConfigParser()

    # 获取配置文件中 URL 的值
    while True:
        try:
            config.read(CONFIGFILE)
            url = config.get('General', 'URL').decode('utf-8')
        except:
            default_config(config, CONFIGFILE)
        else:
            break

    # 模拟浏览器
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) \
                                Gecko/20100101 Firefox/4.0.1'
    headers = { 'User-Agent' : user_agent }
    request = urllib2.Request(url=url, headers=headers)
    # 每个月一个数据库(e.g. 2011_05.db)
    dbfile = time.strftime('%Y_%m',time.localtime()) + '.db' 
    isconnected = False  # 网络连接状态
    starttime = endtime = None
    start = end = None
    sleep_time = 30 # 每次循环的间隔(秒)
    conn = cur = None

    try:
        conn = sqlite3.connect(dbfile)  # 连接数据库
        cur = conn.cursor()  # 获取游标
    except:# Exception, e:
        # print e
        # 建表
        cur.execute('''
        CREATE TABLE time (
          id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT DEFAULT 1,
          starttime TEXT,
          endtime   TEXT,
          totaltime REAL
        )
        ''')
        
    format_time = lambda s : time.strftime('%Y/%m/%d %H:%M:%S', 
                                time.localtime(s))

    while True:
        try:
            urllib2.urlopen(request)
        except:# Exception, e:
            # print e
            # print isconnected
            if isconnected: # 连接第一次断开
                endtime = time.time()
                end = format_time(endtime)
                print 'end: %s' % end
                totaltime = total(starttime, endtime)
                print 'total: %sm' % totaltime
                try:
                    conn = sqlite3.connect(dbfile)  # 连接数据库
                    cur = conn.cursor()  # 获取游标
                    update_data(cur, start, end, totaltime) # 更新数据
                    total_month = query_sum(cur) # 获取当月总上网时间
                except Exception, e:
                    print e
                finally:
                    conn.commit()  # 提交挂起的事务
                    cur.close() # 关闭游标
                    conn.close() # 关闭数据库连接
                print u'当月总上网时间：%s 分钟（%.2f 小时）' % (total_month, total_month/60.0)
                # pass
                isconnected = False # 标记连接状态为断开
        else:
            # print 'ok'
            if not isconnected: # 第一次连接
                starttime = time.time()
                start = format_time(starttime)
                print 'start: %s' % start
                isconnected = True
                endtime = 'None'
                totaltime = 0.0
                try:
                    conn = sqlite3.connect(dbfile)  # 连接数据库
                    cur = conn.cursor()  # 获取游标
                    insert_data(cur, start, endtime, totaltime)
                except Exception, e:
                    print e
                finally:
                    conn.commit()  # 提交挂起的事务
                    cur.close() # 关闭游标
                    conn.close() # 关闭数据库连接
                # print isconnected
                # pass
            else:
                endtime = time.time()
                end = format_time(endtime)
                totaltime = total(starttime, endtime)
                try:
                    conn = sqlite3.connect(dbfile)  # 连接数据库
                    cur = conn.cursor()  # 获取游标
                    update_data(cur, start, end, totaltime)
                except Exception, e:
                    print e
                finally:
                    conn.commit()  # 提交挂起的事务
                    cur.close() # 关闭游标
                    conn.close() # 关闭数据库连接
        time.sleep(sleep_time) # 每过一段时间(秒)循环一次


if __name__ == '__main__':
    main()