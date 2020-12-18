#!/usr/bin/env python
# coding=utf-8

from sanic import Blueprint

from view.index import index
from view.login import login, logout
from view.customer import get_customer_detail
from view.signature import add_signature

view_bp = Blueprint("view_bp")

route_rule_list = [
    # 用户信息搜索页面
    (index, "/"),
    # 登录页面
    (login, "/login"),
    # 登出页面
    (logout, "/logout"),
    (get_customer_detail, "/get/customerDetail"),
    (add_signature, "/put/signatureAdd")
]

for route_rule in route_rule_list:
    view_bp.add_route(*route_rule)
