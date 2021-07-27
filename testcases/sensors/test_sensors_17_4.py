# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/7/16
# @File: test_sensors_17_4.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: sensors_test
# @update: Record important updates
# ---

import os
import unittest
import time
import warnings
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo


'''未完成'''

class DynamicSensorDiscoveryTest(unittest.TestCase):
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
        self.d.unlock()
        print("解锁成功")

    def test_sensors_8_1(self):
        os.system("adb -s " + self.test_device + " shell settings get global bluetooth_on")
        print("启动cts测试应用！")
        os.system("adb -s " + self.test_device + " shell am start -n com.android.cts.verifier/com.android.cts.verifier.CtsVerifierActivity")
        time.sleep(3)
        if self.d.exists(text="Folded") and self.d.exists(resourceId="com.android.cts.verifier:id/export"):
            print("正常进入软件主界面！")
        else:
            self.assertFalse("cts未在主界面，请检查")
        for i in range(100):
            if self.d.exists(text="Companion Device Test"):
                self.d(text="Companion Device Test").click()
                break
            else:
                self.d.swipe(0.5, 0.9, 0.5, 0.2)
                time.sleep(2)
        if self.d.exists(resourceId="android:id/button1"):
            self.d(resourceId="android:id/button1").click()
            time.sleep(1)
        self.d(text="GO").click()
        time.sleep(10)
        for i in range(20):
            if self.d.exists(text="Xperia Ace II"):
                self.d(text="Xperia Ace II").click()
                break
            else:
                self.d.swipe(0.5, 0.6, 0.5, 0.4)
                time.sleep(5)
                if i == 19:
                    self.assertFalse("未找到指定辅助机蓝牙")
        result = self.d(resourceId='com.android.cts.verifier:id/pass_button').info['enabled']
        print(result)
        if result:
            print("测试pass!")
            self.d(resourceId='com.android.cts.verifier:id/pass_button').click()
        else:
            self.assertFalse("测试fail")

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        self.d.app_stop_all()  # 停止所有应用
        self.d.press("home")
        self.d.screen_off()  # 锁屏


if __name__ == '__main__':
    unittest.main()