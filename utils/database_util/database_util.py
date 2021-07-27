# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/3/25
# @File: database_util.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: sql action
# @update: Record important updates
# ---

import pymysql
import configparser
from ..log_util.logcat import LogCat


class DataBase(object):
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.path = './database.conf'
        self.db_info = []
        self.conn = None
        self.db = None
        self.cursor = None
        self.secs = None
        self.log = LogCat()

    def connection(self, host, port, db, user, password):
        # 打开数据库连接
        self.db = pymysql.connect(host=host, user=db, password=user, db=password, port=port, charset='utf8')
        print('数据库连接成功！')
        self.log.console_out(level='info', info='数据库连接成功！')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()
        print("cursor创建成功！")
        self.log.console_out(level='info', info='cursor创建成功！')

    def exec(self, sql):
        # 使用 execute()  方法执行 SQL 查询
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            self.log.console_out(level='info', info=sql + '执行成功！')
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.db.rollback()
            self.log.console_out(level='info', info=sql + '异常回滚！')
        # 使用 fetchone() 方法获取单条数据.
        data = self.cursor.fetchall()
        return data

    def destroy(self):
        # 关闭数据库连接
        self.cursor.close()
        self.db.close()
        self.log.console_out(level='info', info='数据库关闭！')

    def get_db_conf(self):
        # 获取数据库信息
        self.conf.read(self.path)
        # 每个section由[]包裹
        self.secs = self.conf.sections()
        # 获取某个section名为prod所对应的键
        options = self.conf.options("section")
        # 获取[prod]中host对应的值
        for item in options:
            info = self.conf.get("section", item)
            self.db_info.append(info)
        # 获取所有数据库信息
        print(self.db_info)
        return self.db_info


if __name__ == "__main__":
    DataBase = DataBase()
    DataBase.get_db_conf()
