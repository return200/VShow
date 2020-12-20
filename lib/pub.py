#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-11 
# __time__ = 17:53
import random
import re
import string

from sanic import response
from common import tpl_env
from config import ResCode
from lib.pub_cipher import md5_digest

RE_PHONE = re.compile("^(\+86)?1\d{10}$")
RE_TELEPHONE = re.compile("^\d{3,4}?-\d{7,8}$")
RE_EMAIL = re.compile("^[A-Za-z0-9]+([-_.][A-Za-z0-9]+)*@([A-Za-z0-9]+[-.])+[A-Za-z0-9]{2,4}$")
RE_CONTAINS_CHINESE = re.compile("[\u4e00-\u9fa5]")
RE_DOMAIN = re.compile(r"[0-9a-z]-?[0-9a-z]+(.[0-9a-z]-?[0-9a-z]+)?.[a-z]{2,26}", re.IGNORECASE)
RE_ICP_APPROVE = re.compile(r"^[京津冀晋蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼渝川黔滇藏陕甘青宁新]ICP[备证]\d+号[-\d+]?$", re.IGNORECASE)
RE_POLICE_APPROVE = re.compile(r"^[京津冀晋蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼渝川黔滇藏陕甘青宁新]公网安备\d{14,}号$")


def resp_json(status: int = ResCode.OK, count: int = 0, msg: str = None, data=None, headers: dict = None):
    """
    响应json
    :param status: 返回的状态码
    :param count: 总条数
    :param msg: 状态解释
    :param data: 数据
    :param headers:响应头
    :return:
    """
    res = {"code": status, "count": count, "msg": ResCode.desc.get(status)}
    if msg is not None:
        res["msg"] = msg
    if data is not None:
        res["data"] = data
    if count is not None:
        res["count"] = count

    return response.json(res, headers=headers)


def resp_table_json(header, data):
    """
    响应表格类型的数据
    :param header: 表格头
    :param data: 表格数据
    :return:
    """
    res = {
        "resultCode": ResCode.OK,
        "msg": ResCode.desc.get(ResCode.OK),
        "data": {
            "header": header,
            "data": data
        }
    }
    return response.json(res)


def html(request, template_name: str, status=200, **vars):
    """
    渲染并响应网页
    :param request:
    :param template_name:
    :param status:
    :param vars:
    :return:
    """
    vars.update({
        "account_name": request["account_name"],
        "left_menu": request.get("session", {}).get("menu", [])
    })
    body = tpl_env.get_template(template_name).render(vars)
    return response.html(body=body, status=status)


def gen_password(text: str) -> str:
    """
    生成密码
    :param text:
    :return:
    """
    tmp = f"1qaz{text}@WSX"
    result = md5_digest(tmp)
    return result


def contains_chinese(text: str) -> bool:
    """
    文本中是否包含中文
    :param text:
    :return:
    """
    contains = re.match(RE_CONTAINS_CHINESE, text)
    return bool(contains)


def is_valid_email(text: str) -> bool:
    """
    文本是否是有效的邮箱地址
    :param text:
    :return:
    """
    is_valid = re.match(RE_EMAIL, text)
    return bool(is_valid)


def is_valid_phone(text: str) -> bool:
    """
    文本是否是有效的手机号
    :param text:
    :return:
    """
    is_valid = re.match(RE_PHONE, text)
    return bool(is_valid)


def is_valid_telephone(text: str) -> bool:
    """
    文本是否是有效的座机号码
    :param text:
    :return:
    """
    is_valid = re.match(RE_TELEPHONE, text)
    return bool(is_valid)


def is_valid_domain(text: str) -> bool:
    """
    文本是否是有效的域名
    :param text:
    :return:
    """
    is_valid = re.match(RE_DOMAIN, text)
    return bool(is_valid)


def is_valid_icp_approve(text: str) -> bool:
    """
    文本是否是有效的ICP备案号
    :param text:
    :return:
    """
    is_valid = re.match(RE_ICP_APPROVE, text)
    return bool(is_valid)


def is_valid_police_approve(text: str) -> bool:
    """
    文本是否是有效的公安网备案号
    :param text:
    :return:
    """
    is_valid = re.match(RE_POLICE_APPROVE, text)
    return bool(is_valid)


def _is_in_ipv4_range(text, ip_range: tuple) -> bool:
    """
    检测文本是否在指定的IP段内
    :param ip_range: IP段
    :return:
    """
    try:
        start_ip, end_ip = ip_range
        assert is_valid_ipv4(text), "invalid ipv4"
        assert is_valid_ipv4(start_ip), "invalid start ip"
        assert is_valid_ipv4(end_ip), "invalid end ip"

        ip_slice = [int(x) for x in text.split(".")]
        start_ip_slice = [int(x) for x in start_ip.split(".")]
        end_ip_slice = [int(x) for x in end_ip.split(".")]

        for ip_fragment, start_fragment, end_fragment in zip(ip_slice, start_ip_slice, end_ip_slice):
            assert start_fragment <= ip_fragment <= end_fragment, f"{text} out of range {start_ip}-{end_ip}"

        return True
    except Exception as e:
        print(e)
        return False


def is_valid_ipv4(text: str) -> bool:
    """
    检查文本是否是有效的IPv4地址
    :param text:
    :return:
    """
    tmp = text.split(".")
    try:
        assert len(tmp) == 4, "bad length"
        assert all(map(lambda x: 0 <= int(x) <= 255, tmp)), "bad range"
        return True
    except:
        return False


def is_valid_private_ipv4(text: str) -> bool:
    """
    检测文本是否是有效的内网IP
    :param text:
    :return:
    """
    private_ipv4_ranges = [("10.0.0.0", "10.255.255.255"),
                           ("172.16.0.0", "172.31.255.255"),
                           ("192.168.0.0", "192.168.255.255")]
    is_valid = any(map(lambda x: _is_in_ipv4_range(text, x), private_ipv4_ranges))
    return is_valid


def is_valid_public_ipv4(text: str) -> bool:
    """
    检测文本是否是有效的公网IP
    :param text:
    :return:
    """
    return not is_valid_private_ipv4(text)


def random_string(length: int = 10) -> str:
    """
    生成随机字符串
    :param length: 字符串长度
    :return:
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(length)]
    random_str = ''.join(str_list)

    return random_str


if __name__ == '__main__':
    # print(is_valid_domain("178.com"))
    # print(is_valid_icp_approve("京ICP备16021487号-10"))
    print(is_valid_private_ipv4("192.169.1.1"))
