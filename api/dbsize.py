#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : dbsize.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/9/3 0013 19:36
from datetime import datetime

import pandas as pd

from common_enums import YesNoStatus
from config import ResCode, db_file, dbsize_page_limit
from lib.pub import resp_json
from lib.pub_decorator import func_doc
from lib.pub_sqlite import SqliteConnect


@func_doc
async def getsize(request):
    """
    空间增长趋势
    数据格式：
    data = [
        {"host": "172.17.1.3",
         "port": ["3336", "3306"],
         "date": ["Mon", "Tue", "Wen", "Thus", "Fri"],
         "data": [
             {"name": "3306", 'type': 'line', "data": [100, 20, 330, 4550, 2]},
             {"name": "3336", 'type': 'line', "data": [100, 200, 30, 40, 2]},
         ]},
        {"host": "172.17.1.2",
         "port": ["3316", "3306"],
         "date": ["Mon", "Tue", "Wen", "Thus", "Fri"],
         "data": [
             {"name": "3316", 'type': 'line', "data": [100, 20, 330, 4550, 2]},
             {"name": "3306", 'type': 'line', "data": [100, 200, 30, 40, 2]},
         ]},
        {"host": "172.17.1.1",
         "port": ["3316", "3306"],
         "date": ["Mon", "Tue", "Wen", "Thus", "Fri"],
         "data": [
             {"name": "3316", 'type': 'line', "data": [1000, 200, 330, 4550, 2]},
             {"name": "3306", 'type': 'line', "data": [100, 200, 300, 4000, 2]},
         ]},
    ]
    """
    params = request.get("params")
    page = params.get("page")

    print(f"""~~~~ 查询 {(int(page) - 1) * dbsize_page_limit} < server数<= {int(page) * dbsize_page_limit}""")

    sc = SqliteConnect(db_file)

    # 查询server总数，用于前端懒加载，每次刷新查询固定数量的server信息
    sql = f"SELECT COUNT(id) FROM server_list WHERE is_delete={YesNoStatus.NO}"
    res = sc.getresult(sql)
    # 根据每次查询的数量，返回server一共可以分多少页
    server_page = res[0][0] // dbsize_page_limit

    # 1.查出所有实例，ip:port
    sql = f"""
--             SELECT t2.ipaddress, t1.port from instance_list AS t1
            SELECT t2.ipaddress, t1.port from instance_list AS t1
            INNER JOIN server_list AS t2 ON t1.host_id=t2.id
            WHERE t2.is_delete={YesNoStatus.NO}
            AND t1.update_time=(SELECT MAX(server_list.update_time) FROM server_list WHERE is_delete={YesNoStatus.NO})
--             AND t2.is_delete={YesNoStatus.NO};
            """
    instance_list = sc.getresult(sql)

    # 根据前端懒加载查询的页码和每页显示数量返回部分实例列表
    part_instance_host_mark = ""
    part_instance_count = 0
    part_instance_list = []

    for part_instance in instance_list:
        # print(part_instance_count)
        host = part_instance[0]
        if host != part_instance_host_mark:
            part_instance_count += 1

        if (int(page) - 1) * dbsize_page_limit < part_instance_count <= int(page) * dbsize_page_limit:
            part_instance_list.append(part_instance)

        part_instance_host_mark = host

    # print(part_instance_list)

    # 2.根据当前日期生成前N天的日期格式
    now_date = datetime.now().strftime("%m/%d/%Y")
    index = pd.date_range(end=now_date, periods=7)

    # 3.每个实例按日期查询，以列表形式保存，每个实例一行。
    data = []  # data本体
    data_item = dict()  # data中的每个条目
    data_item_port_list = []  # data中每个条目的port列表
    data_item_data_list = []  # data中每个条目的实例列表
    data_item_data_list_item = dict()  # data中每个条目的实例列表中的每个条目

    # 查询部分实例列表的具体信息
    host_mark = ""
    # for instance in instance_list:
    for instance in part_instance_list:
        # print(instance)
        host = instance[0]
        port = instance[1]

        if not host:
            continue

        if data_item and str(host) != str(host_mark):
            # print(data_item)
            data_item_port_list = []
            data_item_data_list = []
            data.append(data_item.copy())

        # print("查询：", host, port)

        data_item["host"] = host
        data_item_port_list.append(str(port))
        data_item["port"] = data_item_port_list
        data_item["date"] = [i.strftime("%Y/%m/%d") for i in index]

        # 按天查询数据，查询条件: ip port
        data_item_data_list_item_data_list = []
        for i in index:
            format_date = i.strftime("%Y/%m/%d")
            # print(f"查询这天：{format_date}")
            sql = f"""
                    SELECT t2.ipaddress,t3.port, sum(t1.db_size), t1.update_time FROM db_list AS t1
                    INNER JOIN server_list AS t2 ON t1.host_id=t2.id
                    INNER JOIN instance_list AS t3 ON t1.port_id=t3.id
                    WHERE t2.ipaddress='{host}' AND t2.is_delete={YesNoStatus.NO} AND t3.port={port}
                    AND t1.update_time=(SELECT MAX(update_time) FROM db_list WHERE update_time LIKE '%{format_date}%');
                    """
            # print(sql)

            res = sc.getresult(sql)
            # print(res)

            res_item = res[0]
            # res_host = res_item[0]
            res_port = res_item[1] or port
            res_size = res_item[2] or 0
            # res_date = res_item[3]

            data_item_data_list_item["name"] = res_port
            data_item_data_list_item["type"] = "line"
            data_item_data_list_item_data_list.append(res_size)
            data_item_data_list_item["data"] = data_item_data_list_item_data_list
        data_item_data_list.append(data_item_data_list_item.copy())
        data_item["data"] = data_item_data_list

        host_mark = host
    else:
        # print(data_item)
        data.append(data_item.copy())

    # print(data)

    return resp_json(status=ResCode.OK, data=data, count=server_page)


async def getrank(request):
    """
    空间占用排名
    :param request:
    :return:
    """
    params = request.get("params")
    page = params.get('page')
    limit = params.get('limit')

    additional_sql = ''
    if len(params) > 2:
        additional_sql += 'AND ('
        for k, v in params.items():
            if k != 'page' and k != 'limit':
                additional_sql += f' {k} LIKE "%{v}%" OR'
        additional_sql = additional_sql.rstrip('OR')
        additional_sql += ')'

    sc = SqliteConnect(db_file)

    sql = f"""
            SELECT t2.ipaddress, t3.port, t3.datadir || '/' || t1.db_name AS datadir, t1.db_size, \
            t1.update_time, t2.comment || ' ' || t3.comment || ' ' || t1.comment AS comment
            FROM db_list AS t1
            INNER JOIN server_list AS t2 ON t1.host_id=t2.id
            INNER JOIN instance_list AS t3 ON t1.port_id=t3.id
            WHERE t1.update_time=(SELECT MAX(db_list.update_time) from db_list)
            AND t2.is_delete={YesNoStatus.NO}
            {additional_sql}
            ORDER BY t1.db_size DESC
            LIMIT ({page}-1)*{limit}, {limit};
            """

    res = sc.getresult(sql)

    count_sql = f"""
            SELECT count(1)
            FROM db_list AS t1
            INNER JOIN server_list AS t2 ON t1.host_id=t2.id
            INNER JOIN instance_list AS t3 ON t1.port_id=t3.id
            WHERE t1.update_time=(SELECT MAX(db_list.update_time) from db_list)
            AND t2.is_delete={YesNoStatus.NO}
            {additional_sql}
            ORDER BY t1.db_size DESC;
            """

    count_res = sc.getresult(count_sql)

    data = []
    for i in res:
        tmp = dict()
        tmp['ipaddress'] = i[0]
        tmp['port'] = i[1]
        tmp['datadir'] = i[2]
        tmp['db_size'] = i[3]
        tmp['update_time'] = i[4]
        tmp['comment'] = i[5]
        data.append(tmp)

    return resp_json(status=ResCode.OK, count=count_res[0][0], data=data)
