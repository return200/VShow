#!/usr/bin/env pythonto
# coding=utf-8
# __project__ = eams
# __author__ = shiyongfei@donews.com
# __date__ = 2018-12-11
# __time__ = 16:36

# 注册表结构

import argparse
from sanic.exceptions import NotFound, Forbidden

from handler.listen_handler import add_listen_handler
from handler.middleware_handler import add_middleware_handler
from bp.api_bp import data_api_bp
from bp.view_bp import view_bp

from lib.log_config import get_logging_config, ACCESS_LOG_FILE_NAME

from sanic import Sanic

LOGGING = get_logging_config(ACCESS_LOG_FILE_NAME)
app = Sanic(log_config=LOGGING)

app.blueprint(data_api_bp)
app.blueprint(view_bp)

app = add_listen_handler(app)
app = add_middleware_handler(app)
app.static('/static', "static")
app.static('/favicon.ico', "static/images/favicon.ico")

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-host', type=str, action='store', dest='host', help='listening host', default="0.0.0.0")
    arg_parser.add_argument('-port', type=int, action='store', dest='port', help='listening port', default=8000)
    arg_parser.add_argument('-debug', type=bool, action='store', dest='debug', help='whether is debug mode',
                            default=False)
    arg_parser.add_argument('-worker', type=int, action='store', dest='worker', help='workers count', default=1)
    args = arg_parser.parse_args()

    host = args.host
    port = args.port
    is_debug = args.debug
    workers_count = args.worker

    app.run(host=host, port=port, debug=is_debug, workers=workers_count)
