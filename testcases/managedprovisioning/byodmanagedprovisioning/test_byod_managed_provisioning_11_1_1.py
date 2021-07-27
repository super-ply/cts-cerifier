# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/3
# @File: test_byod_managed_provisioning_11_1_1.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: test_byod_managed_provisioning自动化测试脚本
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


class ProfileOwnerInstalled(unittest.TestCase):
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

    def test_profile_owner_installed_11_1_1(self):
        # warnings.simplefilter('ignore', ResourceWarning)  # 屏蔽警报信息
        # print("测试开始")
        # print("获取手机设备信息！")
        # self.device = DeviceInfo()
        # self.devices = self.device.check_device()[0]
        # device = self.devices[0]  # 暂时默认只连接一台手机
        # print(device)
        # self.d = u2.connect(device)  # 连接待测设备
        # self.d.unlock()
        # print("解锁成功")
        # print("启动cts测试应用！")
        os.system("adb -s " + self.test_device + " shell am start -n com.android.cts.verifier/com.android.cts.verifier.CtsVerifierActivity")
        time.sleep(5)
        if self.d.exists(text="Folded") and self.d.exists(resourceId="com.android.cts.verifier:id/export"):
            print("正常进入软件主界面！")
        else:
            self.assertFalse("cts未在主界面，请检查")
        for i in range(100):
            if self.d.exists(text="BYOD Managed Provisioning"):
                self.d(text="BYOD Managed Provisioning").click()
                break
            else:
                self.d.swipe(0.5, 0.9, 0.5, 0.2)
                time.sleep(2)
        if self.d.exists(resourceId="android:id/button1"):
            self.d(resourceId="android:id/button1").click()
            time.sleep(1)
        self.d(text="START BYOD PROVISIONING FLOW").click()
        time.sleep(2)
        if self.d.exists(text="CANCEL"):
            self.d(text="CANCEL").click()
        if self.d.exists(text="Accept & continue"):
            self.d(text="Accept & continue").click()
        for i in range(10):
            time.sleep(10)
            if self.d.exists(text="Next"):
                self.d(text="Next").click()
                time.sleep(20)
                break
            if i == 9:
                self.assertFalse("长时间未出现Next按钮！")
        for i in range(100):
            if self.d.exists(text="Profile owner installed"):
                # points = self.d(text="Profile owner installed").info.get("bounds")
                # print(points)
                im = self.d(text="Profile owner installed").screenshot()
                pic_dir_path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "\\report\\pic\\"  # 测试结果图片文件夹保存路径
                now_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                pic_path = pic_dir_path + "test_11_1_1_" + now_time + ".jpg"  # 测试结果图片保存路径
                im.save(pic_path)
                image = Image.open(pic_path)
                image = image.convert('RGB')
                color = PicUtil().get_dominant_color(image)
                print(color)
                # 绿色RGB值范围： 75-100，95-120， 20-40
                # 红色RGB值范围： 120-130， 62-73， 55-65
                R,G,B = color
                if 75 < int(R) < 95 < int(G) < 120 and 20 < int(B) < 40:
                    print("11.1.1测试pass！")
                    return True
                else:
                    self.assertFalse("11.1.1测试fail！")
                break
            else:
                self.d.swipe(0.5, 0.9, 0.5, 0.2)
                time.sleep(2)

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        # self.d.app_stop_all()  # 停止所有应用
        # self.d.press("home")
        # self.d.screen_off()  # 锁屏


if __name__ == '__main__':
    unittest.main()
