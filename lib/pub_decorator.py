#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-24 
# __time__ = 14:57
from functools import wraps


def func_doc(func):
    """
    获取请求处理函数的说明
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        tmp_doc = func.__doc__ or ""
        tmp_doc = tmp_doc.split("\n")
        if len(tmp_doc) > 2:
            doc = tmp_doc[1].strip()
            request["func_doc"] = doc
        else:
            request["func_doc"] = func.__name__

        response = await func(request, *args, **kwargs)
        return response

    return wrapper
