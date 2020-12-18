#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-11 
# __time__ = 15:06
import socket
import struct


def get_ipv4(domain: str) -> list:
    """
    根据域名查询其IPv4地址
    :param domain: 要查询的域名
    :return:
    """
    addr = socket.getaddrinfo(domain, None)
    ipv4s = [x[4][0] for x in addr]
    return ipv4s


def gen_ips(start, end):
    """
    根据ip段生成所有可用ip
    :param start:
    :param end:
    :return:
    """
    ipstruct = struct.Struct('>I')
    start, = ipstruct.unpack(socket.inet_aton(start))
    end, = ipstruct.unpack(socket.inet_aton(end))
    return [socket.inet_ntoa(ipstruct.pack(i)) for i in range(start, end + 1)]


if __name__ == '__main__':
    ip = get_ipv4("www.baidu.com")
    print(ip)
