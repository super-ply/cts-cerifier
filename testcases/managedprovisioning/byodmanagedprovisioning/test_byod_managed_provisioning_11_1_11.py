# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/7/21
# @File: test_byod_managed_provisioning_11_1_10.py
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


class ProfileAwareLocationSettings(unittest.TestCase):
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

    def test_byod_managed_provisioning_11_1_11(self):
        for i in range(10):
            time.sleep(10)
            if self.d.exists(text="Profile-aware location settings"):
                self.d(text="Profile-aware location settings").click()
                time.sleep(2)
                self.d(text="GO").click()
                time.sleep(5)
                self.d(text="Work").click()
                if self.d(text="Location for work profile").exists and self.d(resourceId='android:id/switch_widget').exists:
                    print("Work profile 在界面中存在，同时存在一个可切换的开关")
                    main_location_state = self.d(resourceId="android:id/switch_widget")[0].info
                    if main_location_state['text'] == 'On':
                        self.d(resourceId="android:id/switch_widget")[0].click()
                        work_location_state = self.d(resourceId="android:id/switch_widget")[1].info
                        if work_location_state['text'] == 'Off':
                            print("俩个开关保持一致")
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
                            self.assertFalse("俩个开关不一致")
                    else:
                        self.d(resourceId="android:id/switch_widget")[0].click()
                        work_location_state = self.d(resourceId="android:id/switch_widget")[1].info
                        if work_location_state['text'] == 'On':
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
                            self.assertFalse("俩个开关不一致")
                else:
                    os.system(
                        "adb -s " + self.test_device + " shell am start -n com.android.cts.verifier/com."
                                                       "android.cts.verifier.managedprovisioning."
                                                       "ByodFlowTestActivity")
                    self.d(text="FAIL").click()
                    self.assertFalse("Work profile 在界面中不存在，或者不存在一个可切换的开关")
            else:
                self.d.swipe(0.5, 0.7, 0.5, 0.4)
                time.sleep(2)

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        # self.d.app_stop_all()  # 停止所有应用
        # self.d.press("home")
        # self.d.screen_off()  # 锁屏
