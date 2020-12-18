#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Project: PyCharm
# @File   : export.py
# @Author : gaoyuan@infinities.com.cn
# @Time   : 2020/5/18 0018 18:04


import os
import logging
from sanic import response

from config import db_file
from lib.pub_sqlite import SqliteConnect

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


async def export(request):
    """
    导出全部库文件中的最新结果到一个csv文件中
    :param request:
    :return:
    """
    filename = 'DBSize.csv'
    with open(filename, 'w') as fw:
        for i in os.listdir('/'.join((os.getcwd(), f'{db_file}'))):
            logging.info(f'导出{i}')
        sc = SqliteConnect('/'.join((os.getcwd(), f'{db_file}', i)))
        try:
            res = sc.getresult(
                'select server_n, business, node, ip, create_time from RegistryInfo where create_time=(select max(create_time) from RegistryInfo)')
            for j in res:
                # fw.writelines(f'{j}\r\n')
                fw.write(','.join(j[x] for x in range(len(j))))
                fw.write('\n')
        except Exception as e:
            logging.error(f'{i}导出失败，{e}')
        finally:
            sc.close()
    return await response.file(filename, filename='IceList.csv')
