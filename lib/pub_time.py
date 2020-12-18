#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-11 
# __time__ = 14:31
import datetime
import re
import time
from dateutil.relativedelta import relativedelta

FORMAT_DATE = "%Y-%m-%d"
FORMAT_TIME_HOUR = "%Y-%m-%d %H:00:00"
FORMAT_TIME_MINUTE = "%Y-%m-%d %H:%M:00"
FORMAT_TIME_SECOND = "%Y-%m-%d %H:%M:%S"
FORMAT_TIME_MICRO_SECOND = "%Y-%m-%d %H:%M:%S.%f"
FORMAT_TIME_ISO = "%Y-%m-%dT%H:%M:%SZ"


def str_add_time(time_str, add_years: int = 0, add_months: int = 0, add_days: int = 0, add_hours: int = 0,
                 add_minutes: int = 0, add_seconds: int = 0,
                 fmt: str = "%Y-%m-%d %H:%M:%S"):
    """
    给一个时间字符串进行时间的增减，返回一个新的时间字符串
    :param time_str: 待增减的时间字符串
    :param add_years: 增加的年数
    :param add_months: 增加的月份数
    :param add_days: 增加的天数
    :param add_hours: 增加的小时数
    :param add_minutes: 增加的分钟数
    :param add_seconds: 增加的秒数
    :param fmt: 结果字符串的时间格式
    :return:
    """
    if re.match(r'^\d{4}-\d{2}-\d{2}$', time_str):
        t = datetime.datetime.strptime(time_str, '%Y-%m-%d')
    elif re.match(r'^\d{4}-\d{2}$', time_str):
        t = datetime.datetime.strptime(time_str, '%Y-%m')
    elif re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', time_str):
        t = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
    elif re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', time_str):
        t = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    elif re.match(r'^\d{8}$', time_str):
        t = datetime.datetime.strptime(time_str, "%Y%m%d")
    elif re.match(r'^\d{10}$', time_str):
        t = datetime.datetime.strptime(time_str, "%Y%m%d%H")
    elif re.match(r'^\d{12}$', time_str):
        t = datetime.datetime.strptime(time_str, "%Y%m%d%H%M")
    elif re.match(r'^\d{14}$', time_str):
        t = datetime.datetime.strptime(time_str, "%Y%m%d%H%M%S")
    else:
        return None

    t = t + relativedelta(years=add_years, months=add_months, days=add_days, hours=add_hours, minutes=add_minutes,
                          seconds=add_seconds)
    return t.strftime(fmt)


def now_timestamp(unit: str = "s", rounding: bool = True):
    """
    获取当前时间戳
    :param unit: s: 秒；ms：毫秒
    :param rounding: 是否取整
    :return:
    """
    assert unit in ("s", "ms"), "unit must be `s` or `ms`"
    timestamp = time.time()
    timestamp = timestamp if unit == "s" else timestamp * 1000
    timestamp = int(timestamp) if rounding else timestamp
    return timestamp


def now_time_str(fmt=FORMAT_TIME_SECOND):
    """
    获得现在时间的字符串表示
    :param fmt: 返回的时间格式
    :return:
    """
    return datetime.datetime.now().strftime(fmt)


def future_time_str(add_days=0, add_hours=0, add_minutes=0, add_seconds=0, fmt="%Y-%m-%d"):
    """
    获得未来（过去）时间的字符串表示
    :param add_days:增加的天数
    :param add_hours:增加的小时数
    :param add_minutes:增加的分钟数
    :param add_seconds:增加的秒数
    :param fmt:返回的时间格式
    :return:
    """
    f = datetime.datetime.now() + datetime.timedelta(days=add_days, hours=add_hours, minutes=add_minutes,
                                                     seconds=add_seconds)
    return f.strftime(fmt)


def is_valid_time(time_str: str, fmt: str = FORMAT_DATE) -> bool:
    """
    检查是否是一个有效的时间字符串
    :param time_str:
    :param fmt:
    :return:
    """
    try:
        time.strptime(time_str, fmt)
        return True
    except:
        return False
