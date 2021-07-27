# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/7
# @File: test_sharing _of_requested_bugreport_declined_while_being_taken_11.3.2
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: test_sharing _of_requested_bugreport_declined_while_being_taken_11.3.2自动化测试脚本
# @update: Record important updates
# ---

import os
import unittest
import time
import warnings
import uiautomator2 as u2
from PIL import Image
from utils.device_info_util.device_info import DeviceInfo
from utils.pic_util.pic_util import PicUtil

'''
只写到11.3.1判断是否通过
'''


class SharingOfRequestedBugreportDeclinedWhileBeingTaken(unittest.TestCase):
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

    def test_11_3_2(self):
        print("启动cts测试应用！")
        os.system("adb shell am start -n com.android.cts.verifier/com.android.cts.verifier.CtsVerifierActivity")
        self.assertFalse(self.d.exists(text="Folded") and self.d.exists(resourceId="com.android.cts.verifier:id/export")
                         , "cts未在主界面，请检查")
        for i in range(100):
            if self.d.exists(text="Device Owner Requesting Bugreport Tests"):
                self.d(text="Device Owner Requesting Bugreport Tests").click()
                if self.d.exists(text="Check device owner"):
                    # points = self.d(text="Profile owner installed").info.get("bounds")
                    # print(points)
                    im = self.d(text="Check device owner").screenshot()
                    pic_dir_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/report/pic/"  # 测试结果图片文件夹保存路径
                    now_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                    pic_path = pic_dir_path + "test_11_3_1_" + now_time + ".jpg"  # 测试结果图片保存路径
                    im.save(pic_path)
                    image = Image.open(pic_path)
                    image = image.convert('RGB')
                    color = PicUtil().get_dominant_color(image)
                    print(color)
                    # 绿色RGB值范围： 75-100，95-120， 20-40
                    # 红色RGB值范围： 120-130， 62-73， 55-65
                    R, G, B = color
                    if 75 < int(R) < 95 < int(G) < 120 and 20 < int(B) < 40:
                        print("11.3.1测试pass！")
                        return True
                    else:
                        self.assertFalse("11.1.1测试fail！")
                break
            else:
                self.d.swipe(0.5, 0.9, 0.5, 0.2)
                time.sleep(2)
