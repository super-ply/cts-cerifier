# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 16_1_android_protected_confirmation_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Security16.1 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2
import cv2 as cv
from utils.functions.vulcanadb import *
from utils.functions.compare import Compare

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class AndroidProtectedConfirmationTest(unittest.TestCase):
    def open_projection_widget_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Android Protected Confirmation Test')
        d(text='Android Protected Confirmation Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_projection_widget_test()
        self.check_result()

    def check_result(self):
        temp_pass = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\t_pass.png')
        src_img1 = get_element_img(d, d(resourceId="com.android.cts.verifier:id/sec_protected_confirmation_tee_layout"),
                                   'index.png')
        src_img2 = get_element_img(d, d(resourceId="com.android.cts.verifier"
                                                   ":id/sec_protected_confirmation_strongbox_layout"),
                                   'index.png')
        if Compare.compare_template(src_img1, temp_pass) and Compare.compare_template(src_img2, temp_pass):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)

    def mark_fail(self):
        self.open_projection_widget_test()
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        self.open_projection_widget_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
