#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : hostmanage.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/9/4 0004 18:31
from lib.pub import html


def gethosts(request):
    return html(request, 'host_list.html')


def addhost(request):
    pass
    return html(request, 'host_add.html')
