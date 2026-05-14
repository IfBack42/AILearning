# -*- coding: utf-8 -*-
"""
---------------------------------------------------------logger 简单示例:---------------------------------------------------------------------

import logging
import sys

# 1. 先配置根日志器（兜底用）
logging.basicConfig(
    level=logging.WARNING,
    format='[%(levelname)s] %(message)s',
    encoding='utf-8'
)

# 2. 创建模块专属日志器
#setLevel既给 Logger也給 Handler，但作用不同：
#Logger 的 setLevel：控制哪些级别的日志能被处理（总闸门）
#Handler 的 setLevel：控制该处理器具体处理哪些级别的日志（分开关）

logger = logging.getLogger("app")


# 控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# 文件处理器
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.WARNING)

# 绑定
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 测试
logger.debug("不会输出")      # 级别不够
logger.info("出现在控制台")    # INFO >= console_handler的级别
logger.error("两边都有")      # ERROR >= 所有处理器级别
"""

import logging
import os
import datetime
import pandas as pd

class Logger(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, root_path, log_file_name, loger_name,level='info', fmt='%(asctime)s - %(levelname)s - %(name)s - [%(filename)s]: %(message)s'):
        # 指定日志保存的路径
        self.root_path = root_path

        # 初始logger名称和格式
        self.log_name = log_file_name

        # 初始格式
        self.fmt = fmt

        # 先声明一个 Logger 对象
        self.logger = logging.getLogger(loger_name)

        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))

    def get_logger(self):
        # 指定对应的 Handler 为 FileHandler 对象， 这个可适用于多线程情况
        file_name = os.path.join(self.root_path, self.log_name)
        rotate_handler = logging.FileHandler(file_name, encoding="utf-8", mode="a")

        # Handler 对象 rotate_handler 的输出格式
        formatter = logging.Formatter(self.fmt)
        rotate_handler.setFormatter(formatter)

        # 将rotate_handler添加到Logger
        self.logger.addHandler(rotate_handler)

        return self.logger

if __name__ == '__main__':
    # loggeeer = Logger('../','nima').get_logger()
    # loggeeer.info('nima')
    print(datetime.datetime.now()) #2025-08-22 10:12:58.889619
    print(pd.to_datetime(datetime.datetime.now())) #2025-08-22 10:14:10.062311
    print(pd.to_datetime(datetime.datetime.now()).strftime('%Y%m%d%H%M%S'))

