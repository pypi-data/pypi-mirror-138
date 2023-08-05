# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


__all__ = ['Log']


import time
import logging

from rains.const.const_file import ConstPath
from rains.baseic.decorator import CLASS_SINGLETON_PATERN


# 日志服务 :: 记录器日志级别
_CONFIG_LOGGING_LEVEL = 'DEBUG'

# 日志服务 :: 默认流处理器的日志级别
_CONFIG_BASE_HANDLE_LEVEL = 'INFO'

# 日志服务 :: 文件流处理器的日志级别
_CONFIG_FILE_HANDLE_LEVELS = ['DEBUG', 'INFO', 'ERROR', 'WARNING']

# 日志服务 :: 日志输出格式对象
_CONFIG_OUTPUT_STRUCTURE = logging.Formatter('[%(asctime)s] [%(levelname)7s] %(message)s')


@CLASS_SINGLETON_PATERN
class Log(object):
    """
    [ 日志服务 ]

    * NOT MESSAGE

    """

    _logger: logging.Logger
    """ [ 记录器对象 ] """

    def __init__(self):
        """
        [ 日志服务 ]

        * NOT MESSAGE

        Raises:
            CreationLogLivingError: [ 创建日志实例异常 ]

        """

        try:
            # 创建记录器
            self._logger = logging.getLogger()
            self._logger.setLevel(_CONFIG_LOGGING_LEVEL)
            self._logger.handlers.clear()

            # 创建默认流处理器
            self._creation_base_handle()
            # 创建文件流处理器
            self._creation_file_handle()

        except BaseException as err:
            raise CreationLogLivingError(str(err))

    def debug(self, message: str):
        """
        [ 记录 DEBUG ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的日志信息 ]

        """

        self._logger.debug(message)

    def info(self, message):
        """
        [ 记录 INFO ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的日志信息 ]

        """

        self._logger.info(message)

    def warning(self, message):
        """
        [ 记录 WARNING ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的日志信息 ]

        """

        self._logger.warning(message)

    def error(self, message):
        """
        [ 记录 ERROR ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的日志信息 ]

        """

        self._logger.error(message)

    def critical(self, message):
        """
        [ 记录 CRITICAL ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的日志信息 ]

        """

        self._logger.critical(message)

    def _creation_base_handle(self):
        """
        [ 创建默认流处理器 ]

        * NOT MESSAGE

        """

        # 创建处理器
        base_handle = logging.StreamHandler()
        # 配置日志输出格式
        base_handle.setFormatter(_CONFIG_OUTPUT_STRUCTURE)
        # 设置处理器日志等级
        base_handle.setLevel(_CONFIG_BASE_HANDLE_LEVEL)
        # 注册处理器
        self._logger.addHandler(base_handle)

    def _creation_file_handle(self):
        """
        [ 创建文件流处理器 ]

        * NOT MESSAGE
        
        """

        # 创建当前项目的日志根目录
        if not ConstPath.LOGS.is_dir():
            ConstPath.LOGS.mkdir()

        # 创建当前项目的当天日志存放目录
        date = time.strftime('%Y-%m-%d', time.localtime())
        path = ConstPath.LOGS.joinpath(date)
        if not path.is_dir():
            path.mkdir()

        # 创建文件处理器
        for v in _CONFIG_FILE_HANDLE_LEVELS:

            # 创建处理器
            file_handle = logging.FileHandler(f'{path.joinpath(f"{ v }.log")}')
            # 配置日志输出格式
            file_handle.setFormatter(_CONFIG_OUTPUT_STRUCTURE)
            # 设置处理器的日志等级
            file_handle.setLevel(v)
            # 注册处理器
            self._logger.addHandler(file_handle)


class CreationLogLivingError(Exception):

    def __init__(self, message: str):
        """
        [ 创建日志实例异常 ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的错误信息 ]

        """

        self.message = message
    
    def __str__(self) -> str:

        return f"创建日志实例异常:: { self.message }"
