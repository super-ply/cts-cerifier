# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/9
# @File: 13_5_notification_attention_management_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Notifications13.5 自动化测试脚本
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


class NotificationAttentionManagementTest(unittest.TestCase):
    def open_notification_attention_management_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Notification Attention Management Test')
        d(text='Notification Attention Management Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_notification_attention_management_test()
        self.launch_settings()
        self.check_result()

    def launch_settings(self):
        if d(resourceId="com.android.cts.verifier:id/nls_action_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/nls_action_button").click()
            d.sleep(1)
            if 'Not allowed' == d(resourceId="android:id/title", text="CTS Verifier").sibling(
                    resourceId="android:id/summary").info.get('text'):
                d(resourceId="android:id/title", text="CTS Verifier").click()
                d.sleep(1)
                d(resourceId="android:id/switch_widget").click()
                d.sleep(1)
                if d(resourceId="android:id/button1").exists:
                    d(resourceId="android:id/button1").click()
                    d.sleep(1)
                d.press('back')
                d.sleep(1)
                d.press('back')
                d.sleep(1)

    def check_result(self):
        temp_pass = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\t_pass.png')
        temp_fail = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\t_fail.png')
        pass_count = 0
        while not d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            if pass_count < 6:
                for test_item in test_items:
                    src = get_element_img(d, test_item, 'index.jpg')
                    if Compare.compare_template(src, temp_pass):
                        pass_count += 1
                    elif Compare.compare_template(src, temp_fail):
                        d(resourceId="com.android.cts.verifier:id/fail_button").click()
                        d.sleep(1)
                        raise AssertionError('测试失败,测试项：NOTIFICATION_ATTENTION_MANAGEMENT_TEST')
                if pass_count >= 6:
                    d.swipe(0.5, 0.6, 0.5, 0.4)
                pass_count = 0
        d(resourceId="com.android.cts.verifier:id/pass_button").click()
        d.sleep(1)

    def mark_pass(self):
        d.press("back")
        d.sleep(1)
        d.press("back")
        d.sleep(1)
        self.open_notification_attention_management_test()
        if d(resourceId="com.android.cts.verifier:id/pass_button").exists:
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)

    def mark_fail(self):
        self.open_notification_attention_management_test()
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        self.open_notification_attention_management_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
