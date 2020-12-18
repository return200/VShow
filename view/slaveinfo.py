#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : slaveinfo.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/11/11 0011 18:52
from lib.pub import html


async def getslaveinfo(request):
    return html(request, 'slaveinfo.html')
