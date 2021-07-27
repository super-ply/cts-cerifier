# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/2
# @File: 5_2_1_set_timer_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Clock5.2.1 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2
import cv2 as cv

from utils.functions.imageanalysis import get_similarity
from utils.functions.vulcanadb import *
from utils.functions.openhalcon import OpenHalcon as halcon

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
d = u2.connect()


class SetTimerTest(unittest.TestCase):
    def open_set_timer_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Alarms and Timers Tests')
        d(text='Alarms and Timers Tests').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)
        d(resourceId="android:id/text1", text="Set Timer Test").click()
        d.sleep(1)

    def get_std_image(self):
        """
        查看闹钟界面并保存截图
        :return:
        """
        clock_package = 'com.google.android.deskclock'
        clock_activity = 'com.android.deskclock.DeskClock'
        d.press('home')
        d.sleep(1)
        d.app_start(package_name=clock_package, activity=clock_activity, stop=True)
        d.sleep(2)
        d(resourceId="com.google.android.deskclock:id/tab_menu_timer").click()
        d.sleep(3)
        d.screenshot('5_2_1_1.jpg')
        d.sleep(2)
        return cv.imread('5_2_1_1.jpg')

    def get_cur_image(self):
        d(resourceId="com.android.cts.verifier:id/buttons").click()
        d.sleep(2)
        d.screenshot('5_2_1_2.jpg')
        d.sleep(2)
        return cv.imread('5_2_1_2.jpg')

    def test_main(self):
        img_std = self.get_std_image()
        self.open_set_timer_test()
        img_cur = self.get_cur_image()
        similarity_rate = float(get_similarity(img_std, img_cur))
        print(similarity_rate)
        # 相似度0.98->状态栏变化导致的误差
        if d(resourceId="com.google.android.deskclock:id/tab_menu_timer").info.get('selected') \
                and 'Timer' == d(resourceId="com.google.android.deskclock:id/action_bar_title").info.get('text') \
                and similarity_rate > 0.98:
            d.press('back')
            d.sleep(2)
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            raise AssertionError('测试失败,测试项：SET_TIMER_TEST')


if __name__ == '__main__':
    unittest.main()
