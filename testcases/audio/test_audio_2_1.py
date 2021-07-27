# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/1
# @File: start_all_test.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: audio2.1自动化测试脚本
# @update: Record important updates
# ---

import os
import unittest
import time
import warnings
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo


class Audio(unittest.TestCase):
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

    def test_audio(self):
        print("启动cts测试应用！")
        os.system("adb shell am start -n com.android.cts.verifier/com.android.cts.verifier.CtsVerifierActivity")
        if self.d.exists(text="Folded") and self.d.exists(resourceId="com.android.cts.verifier:id/export"):
            print("正常进入软件主界面！")
        else:
            self.assertFalse("cts未在主界面，请检查")
        self.d(text="Audio Acoustic Echo Cancellation (AEC) Test").click()
        time.sleep(1)
        if self.d.exists(text="Is AEC mandatory in this device?"):
            self.d(text="YES").click()
            time.sleep(1)
        self.d(text="TEST").click()
        for i in range(5):
            time.sleep(15)
            test_result = self.d(resourceId="com.android.cts.verifier:id/audio_aec_test_result").get_text()
            if 'test completed.' in test_result:
                print("测试完成，查看测试结果！")
                if 'All Tests Passed' in test_result:
                    print("测试pass！")
                elif 'fail' in test_result:
                    print("测试fail! 测试详情为：" + test_result)
                break
            print(i)

    def tearDown(self):
        print("测试结束，测试步骤回收！")
        self.d.app_stop_all()  # 停止所有应用
        self.d.screen_off()  # 锁屏


if __name__ == '__main__':
    unittest.main()

