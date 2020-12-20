#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __project__ = eams
# __author__ = leejw2012@163.com
# __date__ = 2018-12-27 
# __time__ = 15:46
from sanic import Blueprint
from api.login import gen_login_vcode, login
from api.customer import get_customer, get_customer_detail, get_customer_weight, add_customer_weight
from api.signature import add_signature

data_api_bp = Blueprint("data_api", url_prefix="/api", strict_slashes=True)

route_rule_list = [

    # 登录部分
    (login, "/login", ["POST"]),
    (gen_login_vcode, "/get/captcha", ["GET"]),
    (get_customer, "/get/customer", ["GET"]),
    (get_customer_detail, "/get/customerDetail", ["GET"]),
    (add_signature, "/put/signatureAdd", ["POST"]),
    (get_customer_weight, "/get/customerWeight", ["GET"]),
    (add_customer_weight, "/put/customerWeightAdd", ["POST"])

    # (getrank, "/get/rank", ["GET"]),
    # (gethosts, "/get/hosts", ["GET"]),
    # (addhost, "/add/host", ["POST"]),
    # (delhost, "/del/host", ["POST"]),
    # (getslaveinfo, "/get/slave", ["GET"]),
    # (switchslavestatus, "/switch/slave",["POST"]),
]

for route_rule in route_rule_list:
    data_api_bp.add_route(*route_rule)

if __name__ == "__main__":
    pass
