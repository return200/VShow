#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-11 
# __time__ = 16:37
import re

from sanic.response import redirect, html

from common import rds_conn
from config import ResCode, AUTH_WHITE_LIST, rds_key_account_permission
from lib.pub import resp_json


async def before_request(request):
    """
    对请求进行预处理
    :param request:
    :return:
    """
    # 参数处理
    params = request.raw_args
    params.update({k: v[0] for k, v in request.form.items()})
    for k, v in params.items():
        if isinstance(v, str):
            params[k] = v.strip()
    try:
        params.update(request.json)
    except:
        pass
    request["params"] = params
    request["account_name"] = request.get("session", {}).get("account_name", "")
    request["account_id"] = request.get("session", {}).get("account_id", "")
    request["sql"] = []

    # 权限认证
    url_path = request.path

    for white_url_rule in AUTH_WHITE_LIST:
        if re.match(white_url_rule, url_path):
            # 在白名单内
            break
    else:
        # 不在白名单内
        rds_key_permission = rds_key_account_permission(request["account_id"])
        account_permission = eval(rds_conn.hgetall(rds_key_permission).get("permission", "{}"))
        api_list = account_permission.get("api", [])
        view_list = account_permission.get("view", [])

        if url_path.startswith("/api"):
            if not api_list:
                # 无权限数据，提示登录
                return resp_json(ResCode.LOGIN_REQUIRED)

            for api in api_list:
                # 需要正则匹配，匹配成功 pass，否则继续查找
                if re.match(api.get("url"), url_path):
                    break
            else:
                # 没找到，无此权限
                return resp_json(ResCode.FORBIDDEN)
        else:
            if not api_list:
                # 无权限数据，清空session，并重定向到登录页
                request["session"].clear()
                rds_conn.delete(rds_key_permission)
                # return html("发呆时间过长，需要重新<a href='#' onclick='parent.location.href=\"/login\"'>登录</a>")
                return redirect("/login")

            for view in view_list:
                # 需要正则匹配，匹配成功 pass，否则继续查找
                if re.match(view.get("url"), url_path):
                    break
            else:
                # 没找到，无此权限，重定向到首页
                return redirect("/home")


def add_middleware_handler(app):
    """
    对 sanic app 添加中间件
    :param app:
    :return:
    """
    app.register_middleware(before_request, "request")
    return app
