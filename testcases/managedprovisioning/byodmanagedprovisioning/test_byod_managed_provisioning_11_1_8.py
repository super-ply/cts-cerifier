# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/4
# @File: test_profile-aware_device_administrator_settings.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: test_profile-aware_device_administrator_settings自动化测试脚本
# @update: Record important updates
# ---

import os
import unittest
import time
import warnings
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo


class ProfileAwareTrustedCredentialSetting(unittest.TestCase):
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

    def test_byod_managed_provisioning_11_1_8(self):
        for i in range(10):
            time.sleep(10)
            if self.d.exists(text="Profile-aware trusted credential settings"):
                self.d(text="Profile-aware trusted credential settings").click()
                time.sleep(2)
                self.d(text="GO").click()
                time.sleep(5)
                for j in range(10):
                    if self.d.exists(text="Credential storage"):
                        self.d(text="Credential storage").click()
                        time.sleep(2)
                        self.d(text="Trusted certificates").click()
                        time.sleep(2)
                        if self.d(text="Personal").exists and self.d(text="Work"):
                            os.system("adb -s " + self.test_device + " shell am start -n com.android.cts.verifier/com."
                                                                     "android.cts.verifier.managedprovisioning."
                                                                     "ByodFlowTestActivity")
                            self.d(text="PASS").click()
                            print("测试PASS！")
                            break
                        else:
                            os.system("adb -s " + self.test_device + " shell am start -n com.android.cts.verifier/com."
                                                                     "android.cts.verifier.managedprovisioning."
                                                                     "ByodFlowTestActivity")
                            self.d(text="FAIL").click()
                            self.assertFalse("credentials list 中未包含 Personal 和 Work 两部分！")
                    else:
                        self.d.swipe(0.5, 0.9, 0.5, 0.2)
                        time.sleep(2)
                break
            else:
                self.d.swipe(0.5, 0.7, 0.5, 0.4)
                time.sleep(2)

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        # self.d.app_stop_all()  # 停止所有应用
        # self.d.press("home")
        # self.d.screen_off()  # 锁屏
