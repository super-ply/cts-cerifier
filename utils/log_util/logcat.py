# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/3/15
# @File: logcat.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: logcat
# @update: Record important updates
# ---

import logging
import os
import datetime


class LogCat(object):
    def __init__(self):
        self.log_path = None
        self.logging = None
        self.path = os.getcwd()

    def console_out(self, level, info):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=self.path + '../../../runtime_log/test.log',
                            filemode='w')
        console = logging.StreamHandler()  # 定义console handler
        console.setLevel(logging.INFO)  # 定义该handler级别
        formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)  # 实例化添加handler
        # 输出日志级别
        if level == 'debug':
            logging.debug(info)
        elif level == 'info':
            logging.info(info)
        elif level == 'warning':
            logging.warning(info)
        elif level == 'error':
            logging.error(info)
        elif level == 'critical':
            logging.critical(info)

    def create_log(self):
        day = datetime.datetime.now()
        grader_father = os.path.abspath(self.path + os.path.sep + "../..")
        path = 'runtime_log/test_' + str(day) + '.log'
        self.log_path = os.path.join(grader_father, path)
        with open(self.log_path, mode='a', encoding='utf-8') as f:
            f.write('Begin Test!' + '\n')

    def record_cts_log(self, line):
        # 逐行写入日志
        with open(self.log_path, mode='a', encoding='utf-8') as f:
            f.write(line + '\n')


if __name__ == "__main__":
    LogCat().console_out(level='warning', info='logging.log')
