#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : hostmanage.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/9/4 0004 18:36
import datetime

from common_enums import YesNoStatus
from config import db_file, ResCode
from lib.pub import resp_json
from lib.pub_sqlite import SqliteConnect


async def gethosts(request):
    pass
    host_list = []
    sc = SqliteConnect(db_file)
    sql = f"SELECT `id`, `domain`, ipaddress, update_time, comment FROM server_list WHERE is_delete={YesNoStatus.NO}"
    res = sc.getresult(sql)

    for i in res:
        tmp = dict()
        tmp["id"] = i[0]
        tmp["domain"] = i[1]
        tmp["ipaddress"] = i[2]
        tmp["update_time"] = i[3]
        tmp["comment"] = i[4]

        host_list.append(tmp)

    return resp_json(status=ResCode.OK, data=host_list)


async def addhost(request):
    now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    params = request.get("params")
    ipaddress = params.get("ipaddress")
    domains = params.get("domains") or ""
    comment = params.get("comment") or ""

    sc = SqliteConnect(db_file)
    sql_check = f"""SELECT 1 FROM server_list WHERE ipaddress='{ipaddress}' AND is_delete={YesNoStatus.NO}"""
    res_check = sc.getresult(sql_check)
    if len(res_check) > 0:
        return resp_json(status=ResCode.PARAM_ERR, msg='该IP已存在')
    else:
        sql = f"""
                INSERT INTO server_list(`domain`, ipaddress, create_time, update_time, comment) 
                VALUES ('{domains}', '{ipaddress}', '{now_date}', '{now_date}', '{comment}')
                """
        try:
            sc.insert(sql)
            return resp_json(status=ResCode.OK, msg='添加成功')
        except Exception as e:
            return resp_json(status=ResCode.SERVER_ERR, msg=e)


async def delhost(request):
    pass
    params = request.get("params")
    host_id = params.get("host_id")

    sc = SqliteConnect(db_file)
    sql = f"""UPDATE server_list SET is_delete={YesNoStatus.YES} WHERE `id`={host_id}"""
    try:
        sc.insert(sql)
        return resp_json(status=ResCode.OK, msg='删除成功')
    except Exception as e:
        return resp_json(status=ResCode.SERVER_ERR, msg=e)
