# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/3/15
# @File: common_util.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: 通用方法
# @update: Record important updates
# ---
# coding=utf-8

import os
import shutil
import datetime

"""
Created on 2020年04月01日
@author: panda
"""


class MyUtil:
    def check_and_creat_folder(self, folder_name):
        # 创建目录
        if os.path.exists(folder_name):
            pass
        else:
            os.makedirs(folder_name)

    def get_today_data(self):
        # 获取当前时间
        data = str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(".", "_").replace(":", "_")
        return data

    def del_file(self, file_path):
        """
        删除文件
        :param filePath: 删除文件的路径
        """
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            pass

    def del_dir_and_file(self, dir_path):
        """
        删除某一目录下的所有文件或文件夹
        :param filepath: 要删除的目录路径
        :return:
        """
        del_list = os.listdir(dir_path)
        for f in del_list:
            file_path = os.path.join(dir_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def check_device_connect(self):
        """
        检查测试机是否连接成功
        :return:
        """
        with os.popen("adb devices") as f:
            text = f.read()
        if "device" in text in text:
            return True
        else:
            return False

    def get_currtime(self):
        """
        获取当前系统时间
        :return:当前时间，格式为 年-月-日 时：分：秒
        """
        curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return curr_time
        pass

    def get_apk_version(self, device, package_name):
        """
        获取apk的版本号
        :return:
        """
        with os.popen(
                "adb -s " + device + " shell dumpsys package " + package_name + " | findstr " + "versionName") as f:
            text = f.read()
        if len(text) > 0:
            version = text.split("=")[1].strip("\n")
        else:
            version = None
        return version
