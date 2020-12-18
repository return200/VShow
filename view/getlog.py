#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : getlog.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/11/19 0019 16:50
from lib.pub import html, random_string


async def getlog(request, _slaveHost):
    randomStr = random_string()
    return html(request, 'xterm.html', slaveHost=_slaveHost, randomStr=randomStr)
