#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-11 
# __time__ = 17:54
from hashlib import sha1, md5


def sha1_digest(text: str) -> str:
    """
    sha1 加密
    :param text:
    :return:
    """
    r = sha1(text.encode("utf8")).hexdigest()
    return r


def md5_digest(text: str) -> str:
    """
    md5 加密
    :param text:
    :return:
    """
    r = md5(text.encode("utf8")).hexdigest()
    return r
