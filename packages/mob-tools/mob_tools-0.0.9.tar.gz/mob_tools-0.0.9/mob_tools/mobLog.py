# !/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time: 2022/2/14 20:46
# @Author: "John"
import platform
from datetime import datetime
from os.path import basename
from loguru import logger
from loguru._get_frame import get_frame

"""
基于loguru的日志模块
"""


def formatted_mob_msg(msg, level, class_name='', func_name='', line_num='', track_id=''):
    """
    :param msg:         日志内容
    :param level:       日志级别
    :param class_name:  调用模块
    :param line_num:    调用行号
    :param func_name:  调用方法名称
    :param track_id:    trackId
    :return:            格式化后的日志内容
    """
    formatted_level = '{0:<8}'.format(f'{level}')
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%S")
    formatted_msg = f'[{ts} {formatted_level}] {class_name}.{func_name}:{line_num} {msg} {track_id}'
    return formatted_msg


class MobLoguru:

    def __init__(self, deep=1, log_file_path="crawler", out_put_level="DEBUG", log_size_limit="200 MB"):
        """

        :param deep:           获取调用者文件名、方法名、行号深度
        :param log_file_path:  输出日志文件路径，默认输出到相对目录下的 crawler_log.log
        :param out_put_level:  限制日志输出最低级别, 默认最低级别为 Debug
        :param log_size_limit: 日志文件大小限制，默认为 200M，超过后会自动拆分、备份
        """
        self._msg = ''
        self._level = ''
        self._track_id = ''
        self._deep = deep
        self._out_put_level = out_put_level
        self._log_size_limit = log_size_limit
        self._sys_platform = platform.system()

        if self._sys_platform == 'Linux':
            # Linux 控制台可以打印日志
            # 但是，同时保存到指定目录一份
            logger.add(f'{log_file_path}.log',
                       # self.log_file = f'{log_file_path}_time:YYYY-MM-DD.log.es'
                       level=self._out_put_level,
                       format="{message}",
                       rotation=self._log_size_limit)

    def debug(self, msg):
        self._msg = msg
        self._level = 'DEBUG'
        return self

    def info(self, msg):
        self._msg = msg
        self._level = 'INFO'
        return self

    def warning(self, msg):
        self._msg = msg
        self._level = 'WARNING'
        return self

    def error(self, msg):
        self._msg = msg
        self._level = 'ERROR'
        return self

    def critical(self, msg):
        self._msg = msg
        self._level = 'CRITICAL'
        return self

    def track_id(self, track_id):
        frame = get_frame(self._deep)
        self._track_id = track_id
        msg = formatted_mob_msg(
            self._msg,
            self._level,
            basename(frame.f_code.co_filename),  # 脚本名称
            frame.f_code.co_name,  # 方法名
            str(frame.f_lineno),  # 行号
            self._track_id
        )

        logger.log(self._level, msg)
        return self

    def commit(self):
        pass
