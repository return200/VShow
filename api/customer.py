#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : customer.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/12/15 0015 10:54
from datetime import datetime

from common import mysql_pool
from common_enums import YesNoStatus
from config import tb_customer, ResCode, tb_customer_detail
from lib.pub import resp_json
from lib.pub_mysql import query_one, query_mysql


async def get_customer(request):
    params = request.get("params")
    user_mobile = params.get("userMobile")

    sql = f"""SELECT COUNT(1) AS count FROM {tb_customer}
            WHERE mobile='{user_mobile}'
            AND is_delete={YesNoStatus.NO}"""
    chk_user_mobile = await query_one(mysql_pool=mysql_pool, sql=sql)

    if not chk_user_mobile.get("count"):
        return resp_json(ResCode.PARAM_ERR, msg='手机号不存在！')

    return resp_json()


async def get_customer_detail(request):
    params = request.get("params")
    page = params.get("page")
    limit = params.get("limit")
    user_mobile = params.get("userMobile")

    customer_detail_sql = f"""SELECT t2.`name`,t2.gender, t2.age, t2.mobile, t2.package, t2.purchase_time,
                                    t1.shape_parts, t1.weight, t1.shape_time, t1.signature
                            FROM {tb_customer_detail} AS t1
                            INNER JOIN {tb_customer} AS t2 on t1.name_id=t2.id
                            WHERE t2.mobile='{user_mobile}' AND t1.is_delete={YesNoStatus.NO}
                            ORDER BY shape_time DESC
                            LIMIT {(int(page) - 1) * int(limit)}, {limit}"""
    print(customer_detail_sql)
    customer_detail_data = await query_mysql(mysql_pool=mysql_pool, sql=customer_detail_sql)

    customer_detail_count_sql = f"""SELECT COUNT(1) as count
                                FROM {tb_customer_detail} AS t1
                                INNER JOIN {tb_customer} AS t2 on t1.name_id=t2.id
                                WHERE t2.mobile='{user_mobile}' AND t1.is_delete={YesNoStatus.NO}"""
    customer_detail_count = await query_one(mysql_pool=mysql_pool, sql=customer_detail_count_sql)

    customer_detail_count = customer_detail_count.get("count") or 0

    if not customer_detail_count:
        return resp_json(ResCode.PARAM_ERR, msg='未查询到用户信息')

    return resp_json(ResCode.OK, count=customer_detail_count, data=customer_detail_data)


async def get_customer_weight(request):
    params = request.get("params")
    user_mobile = params.get("userMobile")

    customer_weight_data = dict()
    customer_weight_tmp_date = []
    customer_weight_tmp_data = dict()
    customer_weight_tmp_data_item = []

    sql = f"""SELECT t1.weight, t1.shape_time 
            FROM {tb_customer_detail} AS t1
            INNER JOIN {tb_customer} AS t2 ON t1.name_id=t2.id
            WHERE t2.mobile='{user_mobile}' AND t1.is_delete={YesNoStatus.NO} AND t2.is_delete={YesNoStatus.NO}
            ORDER BY t1.shape_time DESC
            LIMIT 30"""

    data = await query_mysql(mysql_pool=mysql_pool, sql=sql, request=request)

    for i in data:
        weight = i.get("weight") or 0
        shape_time = i.get("shape_time") or ""

        tmp_date = datetime.strptime(shape_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

        customer_weight_tmp_date.append(tmp_date)
        customer_weight_tmp_data_item.append(weight)

    customer_weight_tmp_data["name"] = "line"
    customer_weight_tmp_data["type"] = "line"
    customer_weight_tmp_data["data"] = customer_weight_tmp_data_item

    customer_weight_data["date"] = customer_weight_tmp_date
    customer_weight_data["data"] = customer_weight_tmp_data

    return resp_json(data=customer_weight_data)
