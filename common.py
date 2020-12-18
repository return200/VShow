#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@infinities.com.cn
# __date__ = 2019-06-10 
# __time__ = 17:38
import pymysql
import redis
from DBUtils.PooledDB import PooledDB
from jinja2 import Environment, select_autoescape, FileSystemLoader

from common_enums import AssetNoDeviceCode
from config import DB_CONFIG, TEMPLATES_DIR, RDS_HOST, RDS_PORT
from lib.pub_mysql import query_one, insert_mysql

mysql_pool = PooledDB(creator=pymysql, **DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
_rds_pool = redis.ConnectionPool(host=RDS_HOST, port=RDS_PORT, decode_responses=True)
rds_conn = redis.Redis(connection_pool=_rds_pool)

tpl_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))
