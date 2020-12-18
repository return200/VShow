#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@infinities.com.cn
# __date__ = 2019-07-31 
# __time__ = 17:24
from sanic.response import redirect

from common import rds_conn
from config import rds_key_account_permission
from lib.pub import html


async def login(request):
    """
    登录页
    :param request:
    :return:
    """
    return html(request, "login.html")


async def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    if "account_id" not in request["session"]:
        return redirect("/login")

    account_id = request["session"]["account_id"]
    request["session"].clear()

    # 删除 redis 中的账户权限信息
    rds_key = rds_key_account_permission(account_id)
    rds_conn.delete(rds_key)

    return redirect("/login")
