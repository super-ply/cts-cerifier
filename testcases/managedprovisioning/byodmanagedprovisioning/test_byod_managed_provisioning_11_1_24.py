# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/7/22
# @File: test_byod_managed_provisioning_11_1_24.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import os
import unittest
import time
import warnings
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo


class AlwaysOnVPNSettings(unittest.TestCase):
    def setUp(self):
        support_device = 'HQ60CT3016'
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

    def test_byod_managed_provisioning_11_1_23(self):
        for i in range(10):
            time.sleep(10)
            if self.d.exists(text="Turn off work profile"):
                self.d(text="Turn off work profile").click()
                time.sleep(2)
                self.d(resourceId="com.android.cts.verifier:id/fail_button").click()
                time.sleep(2)
                self.assertFalse("Cannot establish a VPN connection.This was expected.Mark this test as passed.@")
            else:
                self.d.swipe(0.5, 0.7, 0.5, 0.4)
                time.sleep(2)


    def tearDown(self):
        print("测试结束，测试步骤回收！")
        # self.d.app_stop_all()  # 停止所有应用
        # self.d.press("home")
        # self.d.screen_off()  # 锁屏