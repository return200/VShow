#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __project__ = sanic_data
# __author__ = leejw2012@163.com
# __date__ = 2018-12-18 
# __time__ = 18:49
import sys
import os

# 自定义日志配置 源自sanic.log
# 判断路径是否存在
if not os.path.isdir('./logs'):
    os.mkdir('./logs')
# LOG
ACCESS_LOG_FILE_NAME = './logs/sanic_data'
# 日志保存的数量
BACKUP_COUNT = 30
# 日志切割时间
WHEN = "midnight"
# 日志切割大小
M_SIZE = 1024 * 1024  # 计算M的大小
LOG_SIZE = 100 * M_SIZE  # 保存的单个日志文件的大小


def get_logging_config(filename):
    custom_logging_config = dict(
        version=1,
        disable_existing_loggers=False,
        loggers={
            "root": {
                "level": "INFO",
                "handlers": ["console"]
            },
            "sanic.error": {
                "level": "INFO",
                "handlers": ["error_console"],
                "propagate": True,
                "qualname": "sanic.error"
            },
            "sanic.access": {
                "level": "INFO",
                "handlers": ["access_console"],
                "propagate": True,
                "qualname": "sanic.access"
            },
            "log": {
                "level": "INFO",
                "handlers": ["console", "file_time_handler"]
            },
        },
        handlers={
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stdout
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stderr
            },
            "access_console": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "stream": sys.stdout
            },
            "file_time_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "generic",
                "encoding": "utf-8",
                "filename": filename,
                "backupCount": BACKUP_COUNT,
                "when": WHEN
            },
            "file_size_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "generic",
                "encoding": "utf-8",
                "filename": filename,
                "backupCount": BACKUP_COUNT,
                "maxBytes": LOG_SIZE
            }
        },
        formatters={
            "generic": {
                "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter"
            },
            "access": {
                "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: " +
                          "%(request)s %(message)s %(status)d %(byte)d",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter"
            },
        }
    )

    return custom_logging_config
