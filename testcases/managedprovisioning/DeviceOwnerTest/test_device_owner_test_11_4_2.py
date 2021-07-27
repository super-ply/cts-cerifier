# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/15
# @File: test_device_owner_test_11_4_2
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: test_device_owner_test_11_4_2自动化测试脚本
# @update: Record important updates
# ---

import os
import unittest
import time
import warnings
import uiautomator2 as u2
from PIL import Image
from utils.device_info_util.device_info import DeviceInfo
from utils.pic_util.pic_util import PicUtil
from test_device_owner_test_11_4_1 import CheckDeviceOwner


class DeviceAdministratorSettings(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)  # 屏蔽警报信息
        print("测试开始")
        print("获取手机设备信息！")
        self.device = DeviceInfo()
        self.devices = self.device.check_device()[0]
        device = self.devices[0]  # 暂时默认只连接一台手机
        print(device)
        self.d = u2.connect(device)  # 连接待测设备
        self.d.unlock()
        print("解锁成功")

    def test_11_4_2(self):
        result = CheckDeviceOwner().test_11_4_1()
        print("启动cts测试应用！")
        if result:
            self.d(text="Device administrator settings").click()
            self.d(text="GO").click()
            for i in range(20):
                if self.d.exists(text="Device admin apps"):
                    self.d(text="Device admin apps").click()
                    time.sleep(5)
                    if self.d(text="CTS Verifier").exists:
                        print("CTS Verifier 存在!")
                        info = self.d(text="CTS Verifier").info
                        print(info['clickable'])
                    else:
                        self.assertFalse("CTS Verifier 不存在!")
                    break
                else:
                    self.d.swipe(0.5, 0.9, 0.5, 0.5)
                    time.sleep(2)

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        self.d.app_stop_all()  # 停止所有应用
        for i in range(5):
            self.d.press("back")
        self.d.press("home")
        self.d.screen_off()  # 锁屏


if __name__ == "__main__":
    unittest.main()