# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/2
# @File: start_all_test.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: car4.1自动化测试脚本
# @update: Record important updates
# ---

import os
import unittest
import time
import warnings
import colorsys
import PIL.Image as Image
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo
from utils.pic_util.pic_util import PicUtil


class Car(unittest.TestCase):
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

    def test_car(self):
        print("启动cts测试应用！")
        os.system("adb shell am start -n com.android.cts.verifier/com.android.cts.verifier.CtsVerifierActivity")
        self.assertFalse(self.d.exists(text="Folded") and self.d.exists(resourceId="com.android.cts.verifier:id/export")
                         , "cts未在主界面，请检查")
        for i in range(100):
            if self.d.exists(text="Car Dock Test"):
                self.d(text="Car Dock Test").click()
                break
            else:
                self.d.swipe(0.5, 0.9, 0.5, 0.2)
                time.sleep(2)
        if self.d.exists(resourceId="android:id/button1"):
            self.d(resourceId="android:id/button1").click()
            time.sleep(1)
        self.d(text="ENABLE CAR MODE").click()
        toast_info = self.d.toast.get_message(5, 3, 'Not Found Toast')
        print(toast_info + '\n')
        if 'CAR_DOCK' not in toast_info:
            raise AssertionError('Location 更新的对话框未出现')
        else:
            print('出现Location 更新的对话框')
            self.d.press("home")
            time.sleep(5)
        for i in range(100):
            if self.d.exists(text="Car Dock Test"):
                points = self.d(text="Car Dock Test").info.get("bounds")
                print(points)
                im = self.d(text="Car Dock Test").screenshot()
                im.save("test.jpg")
                image = Image.open('test.jpg')
                image = image.convert('RGB')
                color = PicUtil().get_dominant_color(image)
                print(color)
                # 绿色RGB值范围： 80-90，100-110， 25-35
                # 红色RGB值范围： 120-130， 62-73， 55-65
                R,G,B = color
                if 80 < int(R) < 90 and 100 < int(G) < 110 and 25 < int(B) < 35:
                    print("测试pass！")
                break
            else:
                self.d.swipe(0.5, 0.9, 0.5, 0.2)
                time.sleep(2)

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        self.d.app_stop_all()  # 停止所有应用
        self.d.screen_off()  # 锁屏


if __name__ == '__main__':
    unittest.main()

