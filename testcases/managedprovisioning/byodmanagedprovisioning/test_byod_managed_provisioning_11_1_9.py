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
import configparser
import os
import unittest
import time
import warnings
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo


class ProfileAwareAppSetting(unittest.TestCase):
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

    def test_byod_managed_provisioning_11_1_9(self):
        for i in range(10):
            time.sleep(10)
            if self.d.exists(text="Profile-aware app settings"):
                self.d(text="Profile-aware app settings").click()
                time.sleep(2)
                self.d(text="GO").click()
                time.sleep(10)
                for j in range(10):
                    if self.d.exists(text="Users & accounts"):
                        self.d(text="Users & accounts").click()
                        time.sleep(2)
                        self.d(text="Personal").click()
                        time.sleep(2)
                        self.d(resourceId='android:id/switch_widget').click()
                        if self.d(text="This will conserve data and battery usage, but you will need to sync each "
                                       "account manually to collect recent information, and you will not receive "
                                       "notifications when updates are available.").exists:
                            self.d(text="Cancel").click()
                            time.sleep(2)
                            self.d(text="Work").click()
                            time.sleep(2)
                            self.d(resourceId='android:id/switch_widget').click()
                            time.sleep(2)
                            if self.d(text="This will conserve data and battery usage, but you will need to sync each "
                                           "account manually to collect recent information, and you will not receive "
                                           "notifications when updates are available.").exists:
                                os.system(
                                    "adb -s " + self.test_device + " shell am start -n com.android.cts.verifier/com."
                                                                   "android.cts.verifier.managedprovisioning."
                                                                   "ByodFlowTestActivity")
                                self.d(text="PASS").click()
                                print("测试PASS！")
                                break
                            else:
                                os.system(
                                    "adb -s " + self.test_device + " shell am start -n com.android.cts.verifier/com."
                                                                   "android.cts.verifier.managedprovisioning."
                                                                   "ByodFlowTestActivity")
                                self.d(text="FAIL").click()
                                self.assertFalse("Work选项未弹出警告窗！")
                        else:
                            os.system("adb -s " + self.test_device + " shell am start -n com.android.cts.verifier/com."
                                                                     "android.cts.verifier.managedprovisioning."
                                                                     "ByodFlowTestActivity")
                            self.d(text="FAIL").click()
                            self.assertFalse("Personal选项未弹出警告窗！")
                    else:
                        self.d.swipe(0.5, 0.7, 0.5, 0.4)
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
