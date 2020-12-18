#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : customer.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/12/16 0016 18:04
from common import mysql_pool
from common_enums import YesNoStatus
from config import tb_customer
from lib.pub import html
from lib.pub_mysql import query_one


async def get_customer_detail(request):
    params = request.get('params')
    user_mobile = params.get('userMobile')

    sql = f"""SELECT * FROM {tb_customer} WHERE mobile='{user_mobile}' AND is_delete={YesNoStatus.NO}"""
    customer_info = await query_one(mysql_pool=mysql_pool, sql=sql)

    return html(request, 'customer_detail.html', user_mobile=user_mobile, customer_info=customer_info)
