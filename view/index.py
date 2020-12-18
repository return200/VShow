#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : index.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/12/15 0014 9:56
from lib.pub import html


async def index(request):
    return html(request, 'search.html')
