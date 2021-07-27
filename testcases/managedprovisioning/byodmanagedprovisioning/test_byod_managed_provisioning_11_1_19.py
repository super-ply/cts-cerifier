# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/7/22
# @File: test_byod_managed_provisioning_11_1_17.py
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


class PermissionsLockdown(unittest.TestCase):
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

    def test_byod_managed_provisioning_11_1_19(self):
        apk_path = os.path.abspath(
            os.path.join(os.getcwd(), "..")) + "\\resource\\apk\\CtsPermissionApp.apk"  # 测试结果图片文件夹保存路径
        print(apk_path)
        os.system("adb -s " + self.test_device + " install " + apk_path)
        for i in range(10):
            time.sleep(5)
            if self.d.exists(text="Permissions lockdown"):
                self.d(text="Permissions lockdown").click()
                time.sleep(2)
                self.d(text="GO").click()
                time.sleep(5)
                self.d(text="Grant").click()
                time.sleep(2)
                self.d(text="OPEN APPLICATION SETTINGS").click()
                time.sleep(2)
                self.d(text="Permissions").click()
                time.sleep(2)
                info = self.d(className='android.widget.RelativeLayout')[1].child(resourceId="android:id/title").get_text()
                if info == "Contacts":
                    print("权限被授予！")
                    self.d(text="Contacts").click()
                    time.sleep(2)
                    state = self.d(text="Allow").info['enabled']
                    if not state:
                        print("无法修改！")
                        for i in range(3):
                            self.d.press("back")
                            time.sleep(2)
                        self.d(text="Let user decide").click()
                        time.sleep(2)
                        self.d(text="OPEN APPLICATION SETTINGS").click()
                        time.sleep(2)
                        self.d(text="Permissions").click()
                        time.sleep(2)
                        info = self.d(className='android.widget.RelativeLayout')[1].child(
                            resourceId="android:id/title").get_text()
                        if info == "Contacts":
                            print("权限被授予！")
                            self.d(text="Contacts").click()
                            time.sleep(2)
                            state = self.d(text="Allow").info['enabled']
                            if state:
                                print("可被修改！")
                                for i in range(3):
                                    self.d.press("back")
                                    time.sleep(2)
                                self.d(text="Deny").click()
                                time.sleep(2)
                                self.d(text="OPEN APPLICATION SETTINGS").click()
                                time.sleep(2)
                                self.d(text="Permissions").click()
                                time.sleep(2)
                                info = self.d(className='android.widget.RelativeLayout')[1].child(
                                    resourceId="android:id/title").get_text()
                                if info == 'No permissions allowed':
                                    print("权限未被授予！")
                                    self.d(text="Contacts").click()
                                    time.sleep(2)
                                    state = self.d(text="Allow").info['enabled']
                                    if not state:
                                        print('无法修改！')
                                        for i in range(3):
                                            self.d.press("back")
                                            time.sleep(2)
                                        self.d(text='FINISH').click()
                                        time.sleep(2)
                                        self.d(text="PASS").click()
                                        print("测试PASS！")
                                        break
                                    else:
                                        for i in range(4):
                                            self.d.press("back")
                                            time.sleep(2)
                                        self.d(text="FAIL").click()
                                        time.sleep(2)
                                        self.assertFalse("可以修改！")
                                else:
                                    for i in range(3):
                                        self.d.press("back")
                                        time.sleep(2)
                                    self.d(text="FAIL").click()
                                    time.sleep(2)
                                    self.assertFalse("权限被赠与！")
                            else:
                                for i in range(4):
                                    self.d.press("back")
                                    time.sleep(2)
                                self.d(text="FAIL").click()
                                time.sleep(2)
                                self.assertFalse("无法修改！")
                        else:
                            for i in range(3):
                                self.d.press("back")
                                time.sleep(2)
                            self.d(text="FAIL").click()
                            time.sleep(2)
                            self.assertFalse("权限未被授予！")
                    else:
                        for i in range(4):
                            self.d.press("back")
                            time.sleep(2)
                        self.d(text="FAIL").click()
                        time.sleep(2)
                        self.assertFalse("可被修改！")
                else:
                    for i in range(3):
                        self.d.press("back")
                        time.sleep(2)
                    self.d(text="FAIL").click()
                    time.sleep(2)
                    self.assertFalse("权限未被授予！")
            else:
                self.d.swipe(0.5, 0.7, 0.5, 0.4)
                time.sleep(2)

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        # self.d.app_stop_all()  # 停止所有应用
        # self.d.press("home")
        # self.d.screen_off()  # 锁屏
