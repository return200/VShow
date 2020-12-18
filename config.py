#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __project__ = sanic_data
# __author__ = leejw2012@163.com
# __date__ = 2018-10-26 
# __time__ = 15:39

import os
import sys

from lib.pub_time import now_time_str

# 不用权限认证的 URL path 规则，用正则表示
AUTH_WHITE_LIST = [
    "^/favicon.ico$",
    "^/static/",
    "^/login$",
    "^/logout$",
    "^/err/(forbidden|not_found)$",
    "^/api/get/captcha$",
    "^/api/login$",
    "^/api/export$",
    "^/*"

]

# session 过期时间，1天
SESSION_EXPIRES = 86400

# redis 节点
RDS_HOST = "127.0.0.1"
RDS_PORT = 6379

# ES 节点
ELASTIC_SERVER = ['bjxg-bigdata-es01:9200', 'bjxg-bigdata-es02:9200', 'bjxg-bigdata-es03:9200']

DB_CONFIG = {
    # "host": "192.168.71.21",
    "host": "127.0.0.1",
    # "host": "mysql-eams",
    "port": 3306,
    "user": "vshow",
    "password": "1qaz2wsx3edc",
    "db": "vshow"
}

rds_key_vcode_login = lambda session: f"vshow:vcode:login:{session}"
# 账户权限数据，hash

rds_key_account_permission = lambda account_id: f"vshow:permission:{account_id}"


class EMAIL:
    USERNAME = "test@163.com"
    PASSWORD = "12345"
    SERVER = "smtp.163.com"
    PORT = "654"


class ResCode:
    """
    API 响应状态码
    """
    OK = 0
    PARAM_ERR = 1
    PARAM_NOT_ENOUGH = 2
    NOT_FOUND = 3
    FORBIDDEN = 4
    SERVER_ERR = 5
    LOGIN_REQUIRED = 6

    desc = {
        OK: "成功",
        PARAM_ERR: "参数错误",
        PARAM_NOT_ENOUGH: "参数不完整",
        NOT_FOUND: "不存在",
        FORBIDDEN: "受限，无权限",
        SERVER_ERR: "服务器错误",
        LOGIN_REQUIRED: "请登录",
    }


TEMPLATES_DIR = "templates"

# 账户与权限
tb_account = "account"
tb_role = "role"
tb_page = "sys_page"
tb_api = "sys_api"
tb_role_menu = "role_menu"
tb_role_account = "role_account"
tb_role_api = "role_api"
tb_role_page = "role_page"
tb_slave_info = "slave_info"
tb_customer = "customer_list"
tb_customer_detail = "customer_detail"

db_file = os.path.join("db", "database.db")

# 每次查询db增长趋势的主机数
dbsize_page_limit = 3
