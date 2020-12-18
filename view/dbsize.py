#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : dbsize.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/9/3 0012 17:53
from config import db_file
from lib.pub import html
from lib.pub_sqlite import SqliteConnect
from common_enums import YesNoStatus


async def getsize(request):
    return html(request, 'dbsize.html', res={})


async def getrank(request):
    return html(request, 'dbrank.html')


async def getsummary(request):
    sc = SqliteConnect(db_file)
    time_sql = f"SELECT MAX(update_time) from db_list"
    host_sql = f"SELECT COUNT(1) FROM server_list WHERE is_delete={YesNoStatus.NO}"
    instance_sql = "SELECT COUNT(1) FROM instance_list WHERE update_time=(SELECT MAX(update_time) from instance_list);"
    db_sql = "SELECT COUNT(1) FROM db_list WHERE update_time=(SELECT MAX(update_time) from db_list);"
    size_sql = "SELECT SUM(db_size) FROM db_list WHERE update_time=(SELECT MAX(update_time) from db_list);"

    time_res = sc.getresult(time_sql)
    host_res = sc.getresult(host_sql)
    instance_res = sc.getresult(instance_sql)
    db_res = sc.getresult(db_sql)
    size_res = sc.getresult(size_sql)

    update_time = time_res[0][0]
    host_count = host_res[0][0]
    instance_count = instance_res[0][0]
    db_count = db_res[0][0]
    db_size = size_res[0][0]

    return html(request, 'summary.html', update_time=update_time, host_count=host_count, instance_count=instance_count,
                db_count=db_count, db_size=db_size)
