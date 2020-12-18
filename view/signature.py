#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : signature.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/12/17 0017 17:53
from lib.pub import html


async def add_signature(request):
    params = request.get('params')
    customer_name = params.get('customer_name')
    customer_mobile = params.get('customer_mobile')
    shape_time = params.get('shape_time')

    return html(request, 'signature_add.html',
                customer_name=customer_name,
                customer_mobile=customer_mobile,
                shape_time=shape_time)
