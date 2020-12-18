#!/usr/bin/env python
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-11 
# __time__ = 16:57

import aioredis
from logging import getLogger
from sanic_session import AIORedisSessionInterface, Session

from config import SESSION_EXPIRES, RDS_HOST, RDS_PORT

session = Session()


async def before_server_start(app, loop):
    """
    服务启动前，预处理
    :param app:
    :param loop:
    :return:
    """
    redis_conn = await aioredis.create_redis_pool(address=f"redis://{RDS_HOST}:{RDS_PORT}", loop=loop)
    # 日志对象
    app.log = getLogger("log")
    app.log.info("SERVER_START")
    session.init_app(app, interface=AIORedisSessionInterface(redis_conn, expiry=SESSION_EXPIRES))


async def notify_server_started(app, loop):
    print('Server successfully started.')


async def notify_server_stopping(app, loop):
    print('Server shutting down...')


async def notify_server_stopped(app, loop):
    print('Server successfully shutdown.')


def add_listen_handler(app):
    app.register_listener(before_server_start, "before_server_start")
    app.register_listener(notify_server_started, "after_server_start")
    app.register_listener(notify_server_stopping, "before_server_stop")
    app.register_listener(notify_server_stopped, "after_server_stop")
    return app
