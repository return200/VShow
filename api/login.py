#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : login.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/4/13 0013 17:18


from sanic import response

from common import mysql_pool, rds_conn
from common_enums import YesNoStatus, UseStatus
from config import ResCode, rds_key_account_permission
from lib.pub import resp_json, gen_password
from lib.pub_captcha import get_gif_captcha
from lib.pub_mysql import query_one, query_mysql, insert_mysql
from lib.pub_time import future_time_str, FORMAT_TIME_SECOND, now_time_str


def _get_menu_list(menus: list, parent_id: int = 0) -> list:
    result = []
    for item in menus:
        if item.get('p_id') == parent_id:
            tmp = {
                "id": item.get("id"),
                "name": item.get("name"),
                "icon": item.get("icon"),
                "url": item.get("url"),
                "sort": item.get("sort"),
                "children": _get_menu_list(menus, item.get("id"))
            }
            result.append(tmp)

    result = sorted(result, key=lambda x: x.get("sort"), reverse=False)
    return result


async def login(request):
    """:
    登录
    :param request:
    :return:
    """
    params = request.get("params")
    email = params.get("email")
    password = params.get("password")
    captcha = params.get("captcha")

    if not all((email, password, captcha)):
        return resp_json(status=ResCode.PARAM_ERR, msg="请填写完整")

    real_vcode = request.get("session", {}).get("login_vcode")
    login_vcode_expire_time = request.get("session", {}).get("login_vcode_expire")

    request["session"]["login_vcode"] = None
    request["session"]["login_vcode_expire"] = None

    if not real_vcode or now_time_str(fmt=FORMAT_TIME_SECOND) > login_vcode_expire_time:
        # 没有验证码，失效或根本就没有
        return resp_json(ResCode.PARAM_ERR, msg="请重新获取验证码")

    if captcha != real_vcode:
        # 验证码不一致
        # 之前的验证码进行失效
        return resp_json(ResCode.PARAM_ERR, msg="验证码错误")

    # todo 失败 3 次，1个小时内禁止登录

    password_cipher = gen_password(password)
    sql = f"""SELECT id,user_name,status FROM account WHERE email='{email}' and passwd='{password_cipher}' """
    user = await query_one(mysql_pool, sql)
    if not user:
        return resp_json(ResCode.FORBIDDEN, msg="用户名或密码错误")

    if user.get("status") == UseStatus.NO:
        return resp_json(ResCode.FORBIDDEN, msg="您的账户已被禁用")

    account_id = user.get("id")
    user_name = user.get("user_name")

    sql_auth_page = f"""SELECT sys_page.*
                            FROM sys_page
                            INNER JOIN role_page ON sys_page.id=role_page.page_id
                            INNER JOIN role_account ON role_page.role_id=role_account.role_id
                        WHERE role_account.account_id={account_id}"""
    view_list = await query_mysql(mysql_pool, sql_auth_page)
    menu_list = [x for x in view_list if x.get("is_menu") == YesNoStatus.YES]
    menu_list = _get_menu_list(menu_list)
    if not menu_list:
        # 没有被分配权限
        return resp_json(ResCode.FORBIDDEN, msg="您还没有被分配权限，请确认分配权限后再登录")

    sql_auth_api = f"""SELECT sys_api.*
                            FROM sys_api
                            INNER JOIN role_api ON sys_api.id=role_api.api_id
                            INNER JOIN role_account ON role_api.role_id=role_account.role_id
                            WHERE role_account.account_id={account_id}"""
    api_list = await query_mysql(mysql_pool, sql_auth_api)

    sql_ws_api = f"""SELECT sys_ws.*
                        FROM sys_ws 
                        INNER JOIN role_ws ON sys_ws.id=role_ws.ws_id
                        INNER JOIN role_account ON role_ws.role_id=role_account.role_id
                        WHERE role_account.account_id={account_id}"""
    ws_list = await query_mysql(mysql_pool, sql_ws_api)

    permission = {
        "view": view_list,
        "api": api_list,
        "ws": ws_list,
    }

    rds_key = rds_key_account_permission(account_id)
    permission_data = {
        "permission": permission,
        "menu": menu_list,
        "account_id": account_id,
        "account_name": user_name,
    }
    rds_conn.hmset(rds_key, permission_data)
    rds_conn.expire(rds_key, 60 * 60 * 24)  # 有效期，24小时

    request["session"]["menu"] = menu_list
    request["session"]["account_id"] = account_id
    request["session"]["account_name"] = user_name

    # 清空验证码数据
    request["session"]["login_vcode"] = None
    request["session"]["login_vcode_expire"] = None

    return resp_json()


async def gen_login_vcode(request):
    """
    生成动态验证码
    :param request:
    :return:
    """
    img, vcode = get_gif_captcha()
    print(vcode)
    # Redis 中写入验证码数据，有效期3分钟
    request["session"]["login_vcode"] = vcode
    request["session"]["login_vcode_expire"] = future_time_str(add_seconds=60 * 3, fmt=FORMAT_TIME_SECOND)
    headers = {
        "Pragma": 'no-cache',
        "Content-Type": "image/png",
        "Cache-Control": 'post-check=0, pre-check=0,private, max-age=0, no-store, no-cache, must-revalidate'
    }
    return response.raw(img, headers=headers)
