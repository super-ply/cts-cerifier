# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/4
# @File: test_byod_provisioning_tests_11_2_1
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: test_byod_provisioning_tests_11_2_1自动化测试脚本
# @update: Record important updates
# ---

import os
import unittest
import time
import warnings
import PIL.Image as Image
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo
from testcases.byodmanagedprovisioning.test_byod_managed_provisioning_11_1_1 import ProfileOwnerInstalled
from utils.pic_util.pic_util import PicUtil


"""
    顶部任务栏绿色判断，未做完
"""

class CustomProvisioningColor(unittest.TestCase):
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

    def test_custom_provisioning_color(self):
        for i in range(10):
            if self.d.exists(text="BYOD Provisioning tests"):
                self.d(text="BYOD Provisioning tests").click()
                time.sleep(2)
                self.d(text="Custom provisioning color").click()
                time.sleep(2)
                self.d(text="GO").click()
                time.sleep(2)
                if self.d.exists(classname="android.widget.FrameLayout"):
                    im = self.d.screenshot(classname="android.widget.FrameLayout")
                    now_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                    pic_dir_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/report/pic/"  # 测试结果图片文件夹保存路径
                    pic_path = pic_dir_path + "test_11_2_1_" + now_time + ".jpg"  # 测试结果图片保存路径
                    im.save(pic_path)
                else:
                    print("未截图")
            else:
                self.d.swipe(0.5, 0.9, 0.5, 0.2)
                time.sleep(2)


    def tearDown(self):
        print("测试结束，测试步骤回收！")
        self.d.app_stop_all()  # 停止所有应用
        self.d.press("home")
        self.d.screen_off()  # 锁屏
