#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : slaveinfo.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/11/11 0011 17:19
from common import mysql_pool
from common_enums import YesNoStatus
from config import ResCode, tb_slave_info
from lib.pub import resp_json
from lib.pub_mysql import query_mysql, query_one, update_mysql


async def getslaveinfo(request):
    params = request.get("params")
    page = params.get("page")
    limit = params.get("limit")

    additional_sql = ' WHERE 1=1 '
    if len(params) > 2:
        additional_sql += 'AND ('
        for k, v in params.items():
            if k != 'page' and k != 'limit':
                additional_sql += f' {k} LIKE "%{v}%" OR'
        additional_sql = additional_sql.rstrip('OR')
        additional_sql += ')'

    sql = f"""SELECT slave_host, 
                    slave_port,
                    slave_instance_datadir, 
                    slave_instance_datasize, 
                    slave_instance_inused,
                    slave_backup_state,
                    master_host,
                    master_port,
                    update_time
            FROM slave_info
            {additional_sql}
            ORDER BY slave_host, slave_port
            LIMIT {(int(page) - 1) * int(limit)}, {limit}
        """
    print(sql)
    slave_info = await query_mysql(mysql_pool=mysql_pool, sql=sql)

    for i in slave_info:
        i["update_time"] = i.get("update_time").strftime("%Y-%m-%d %H:%M:%S")

    sql = f"SELECT COUNT(1) AS count FROM slave_info {additional_sql};"
    slave_count = await query_one(mysql_pool=mysql_pool, sql=sql)

    return resp_json(status=ResCode.OK, count=slave_count.get('count'), data=slave_info)


async def switchslavestatus(request):
    params = request.get("params")
    slave_host = params.get("slaveHost")
    slave_port = params.get("slavePort")
    status = 1 if params.get("action") == "start" else 0

    sql = f"""UPDATE slave_info 
            SET slave_instance_inused={status} 
            WHERE slave_host='{slave_host}' AND slave_port={slave_port}
        """

    res = await update_mysql(pool=mysql_pool,
                             tb_name=f"{tb_slave_info}",
                             data={"slave_instance_inused": status},
                             condition={"slave_host": slave_host, "slave_port": slave_port}
                             )

    if res != 0:
        return resp_json(status=ResCode.OK)
    else:
        return resp_json(status=ResCode.SERVER_ERR)
