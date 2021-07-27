# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/3/25
# @File: conf_read.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---

# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/3/15
# @File: config_util.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: 配置文件通用方法先写点
# @update: Record important updates
# ---
import configparser
import os

current_path = os.getcwd()
conf_path = os.path.abspath(os.path.join(current_path, "../..", 'conf/'))


class ConfigReader(object):
    # 配置文件类
    def __init__(self):
        # 初始化配置文件类
        self.info = []
        self.options = []
        self.path = None
        self.secs = None
        self.conf = configparser.ConfigParser()

    def read_conf(self, file, section):
        # 读取配置文件
        self.conf.read(conf_path + file, encoding="utf-8-sig")  # 文件路径
        print(conf_path + file)
        # 每个section由[]包裹
        self.secs = self.conf.sections()
        # 获取某个section名为prod所对应的键
        self.options = self.conf.options(section)
        # 获取[prod]中host对应的值
        for item in self.options:
            info = self.conf.get(section, item)
            self.info.append(info)
        # 获取所有数据库信息
        print(self.info)
        return self.options, self.info

    def read_conf_to_dict(self, file, section):
        conf_dict = {}
        # 读取配置文件
        self.conf.read(conf_path + file, encoding="utf-8-sig")  # 文件路径
        print(conf_path + file)
        # 每个section由[]包裹
        self.secs = self.conf.sections()
        # 获取某个section名为prod所对应的键
        self.options = self.conf.options(section)
        # 获取[prod]中host对应的值
        for item in self.options:
            info = self.conf.get(section, item)
            conf_dict[item] = info
        # 获取所有数据库信息
        return conf_dict


if __name__ == "__main__":
    ConfigReader = ConfigReader()
    ConfigReader.read_conf(file='database.conf', section='section')
