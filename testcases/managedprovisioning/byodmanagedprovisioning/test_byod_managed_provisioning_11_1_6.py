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
import PIL.Image as Image
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo
from utils.pic_util.pic_util import PicUtil


class ProfileAwareDeviceAdministratorSettings(unittest.TestCase):
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

    def test_profile_aware_device_administrator_settings(self):
        for i in range(10):
            time.sleep(10)
            if self.d.exists(text="Profile-aware accounts settings"):
                self.d(text="Profile-aware accounts settings").click()
                time.sleep(2)
                self.d(text="GO").click()
                time.sleep(5)
                for j in range(10):
                    if self.d.exists(text="Users & accounts"):
                        self.d(text="Users & accounts").click()
                        time.sleep(2)
                        if self.d.exists(text="Personal") and self.d.exists(text="Work"):
                            print("Personal 及 Work categories 两者都存在!")
                            if self.d.exists(text="Work"):
                                self.d(text="Work").click()
                                if self.d.exists(text="Remove work profile") or self.d.exists(text="Uninstall"):
                                    print("Remove work profile 或 Uninstall 存在，测试pass！")
                                    os.system("adb -s " + self.test_device + " shell am start -n com.android.cts."
                                                                             "verifier/com.android.cts.verifier"
                                                                             ".managedprovisioning.ByodFlowTestActivity")
                                    self.d(text="PASS").click()
                                    print("测试PASS！")
                                else:
                                    self.assertFalse("未发现 Remove work profile 或 Uninstal,测试fail!")
                                    os.system("adb -s " + self.test_device + " shell am start -n com.android.cts."
                                                                             "verifier/com.android.cts.verifier"
                                                                             ".managedprovisioning.ByodFlowTestActivity")
                                    self.d(text="FAIL").click()
                                    print("测试FAIL！")
                        else:
                            self.assertFalse("未发现 Personal 或 Work categories")
                            self.d.press("back")
                            self.d.press("back")
                            self.d(text="FAIL").click()
                            print("测试FAIL！")
                        break
                    else:
                        self.d.swipe(0.5, 0.9, 0.5, 0.2)
                        time.sleep(2)
                        if j == 9:
                            os.system(
                                "adb -s " + self.test_device + " shell am start -n com.android.cts.verifier/com."
                                                               "android.cts.verifier.managedprovisioning."
                                                               "ByodFlowTestActivity")
                            self.d(text="FAIL").click()
                            self.assertFalse("未找到Users & accounts 选项，请检查！")
                break
            else:
                self.d.swipe(0.5, 0.9, 0.5, 0.2)
                time.sleep(2)

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        # self.d.app_stop_all()  # 停止所有应用
        # self.d.press("home")
        # self.d.screen_off()  # 锁屏
