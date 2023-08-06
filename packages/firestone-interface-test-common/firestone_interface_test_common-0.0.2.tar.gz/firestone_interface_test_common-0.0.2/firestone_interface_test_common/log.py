# coding=utf-8
'''
Created on 2021/11/23 10:37
__author__= yanghong
__remark__=
'''
import os
import time
from loguru import logger
from src.common.tools import get_project_root_path

t = time.strftime("%Y-%m-%d")
LOG_DIR = os.path.join(get_project_root_path("logs"))


class Loggings:
    """日志定义"""
    __instance = None
    logger.add(f"{LOG_DIR}/{t}.log", rotation="100MB", encoding="utf-8", enqueue=True,
               retention="7 days", backtrace=False)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance


loggings = Loggings()
if __name__ == '__main__':
    pass
