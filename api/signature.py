#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : signature.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/12/18 0018 13:53
from common import mysql_pool
from common_enums import YesNoStatus
from config import tb_customer_detail, tb_customer, ResCode
from lib.pub import resp_json
from lib.pub_mysql import raw_update_mysql


async def add_signature(request):
    pass
    params = request.get("params")
    customer_mobile = params.get("customer_mobile")
    customer_name = params.get("customer_name")
    shape_time = params.get("shape_time")
    signature = params.get("signature")

    sql = f"""UPDATE {tb_customer_detail} AS t1
            INNER JOIN {tb_customer} AS t2 ON t1.name_id=t2.id
            SET t1.signature='{signature}'
            WHERE t1.shape_time='{shape_time}'
            AND t2.mobile={customer_mobile}
            AND t2.name='{customer_name}'
            AND t1.is_delete={YesNoStatus.NO}
            AND t2.is_delete={YesNoStatus.NO}"""

    print(sql)
    res = await raw_update_mysql(mysql_pool, sql, request)

    if res == 0:
        return resp_json(ResCode.NOT_FOUND, msg='未查询到该条塑形记录')

    return resp_json()
