# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/6
# @File: test_byod_provisioning_tests_11_2_3
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: test_byod_provisioning_tests_11_2_3自动化测试脚本
# @update: Record important updates
# ---

import os
import unittest
import time
import warnings
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo


class CustomTerms(unittest.TestCase):
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

    def test_custom_terms(self):
        print("启动cts测试应用！")
        os.system("adb shell am start -n com.android.cts.verifier/com.android.cts.verifier.CtsVerifierActivity")
        self.assertFalse(self.d.exists(text="Folded") and self.d.exists(resourceId="com.android.cts.verifier:id/export")
                         , "cts未在主界面，请检查")
        for i in range(10):
            if self.d.exists(text="BYOD Provisioning tests"):
                self.d(text="BYOD Provisioning tests").click()
                time.sleep(2)
                self.d(text="Custom terms").click()
                time.sleep(2)
                self.d(text="GO").click()
                time.sleep(2)
                self.d(text="View terms").click()
                time.sleep(2)
                self.d(text="Company ABC").click()
                time.sleep(2)
                if self.d.exists(text="Company Terms Content. "):
                    print("验证段落内容 Company Terms Content存在，测试pass！")
                    self.d.press("back")
                    time.sleep(2)
                    self.d.press("back")
                    time.sleep(2)
                    if self.d.exists(text="Stop setting up?"):
                        self.d(text="YES").click()
                        time.sleep(2)
                    self.d(resourceId="com.android.cts.verifier:id/pass_button").click()
                else:
                    self.d.press("back")
                    time.sleep(2)
                    self.d.press("back")
                    time.sleep(2)
                    if self.d.exists(text="Stop setting up?"):
                        self.d(text="YES").click()
                        time.sleep(2)
                    self.d(resourceId="com.android.cts.verifier:id/fail_button").click()
                    self.assertFalse("验证段落内容 Company Terms Content不存在，测试fail！")
                break
            else:
                self.d.swipe(0.5, 0.9, 0.5, 0.2)
                time.sleep(2)

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        self.d.app_stop_all()  # 停止所有应用
        self.d.press("home")
        self.d.screen_off()  # 锁屏