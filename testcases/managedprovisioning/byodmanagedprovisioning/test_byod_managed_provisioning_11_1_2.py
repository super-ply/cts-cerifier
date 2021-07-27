# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/3
# @File: test_byod_managed_provisioning_11_1_2.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: test_byod_managed_provisioning自动化测试脚本
# @update: Record important updates
# ---
import configparser
import os
import unittest
import time
import warnings
import PIL.Image as Image
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo
from utils.pic_util.pic_util import PicUtil


class FullDiskEncryptionEnable(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read(os.getcwd() + '/config', encoding='utf-8')
        support_device = config.get('support_device', 'device')
        print(support_device)
        warnings.simplefilter('ignore', ResourceWarning)  # 屏蔽警报信息
        print("测试开始")
        print("获取手机设备信息！")
        self.device = DeviceInfo()
        print(support_device)
        self.devices = self.device.check_device()[0]
        self.devices.remove(support_device)
        self.test_device = self.devices[0]
        self.d = u2.connect(self.test_device)  # 连接待测设备
        # self.d.unlock()
        # print("解锁成功")

    def test_full_disk_encryption_enable_11_1_2(self):
        # result = ProfileOwnerInstalled().test_profile_owner_installed_11_1_1()
        # if result:
        #     self.d(text="Full disk encryption enabled").click()
        #     time.sleep(15)
        self.d(text="Full disk encryption enabled").click()
        time.sleep(15)
        im = self.d(text="Full disk encryption enabled").screenshot()
        pic_path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "\\report\\pic\\"  # 测试结果图片文件夹保存路径
        im.save(pic_path + "test_11_1_2.jpg")
        image = Image.open(pic_path + "test_11_1_2.jpg")
        image = image.convert('RGB')
        color = PicUtil().get_dominant_color(image)
        print(color)
        # 绿色RGB值范围： 75-100，95-120， 25-35
        # 红色RGB值范围： 120-130， 62-73， 55-65
        R, G, B = color
        if 75 < int(R) < 95 < int(G) < 120 and 22 < int(B) < 40:
            print("11.1.2测试pass！")
            return True
        else:
            self.assertFalse("11.1.2测试fail！")

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        # self.d.app_stop_all()  # 停止所有应用
        # self.d.press("home")
        # self.d.screen_off()  # 锁屏

