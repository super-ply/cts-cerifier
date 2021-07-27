# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/9
# @File: 10_1_instant_apps_notification_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS InstantApps10.1 自动化测试脚本
# @update: Record important updates
# ---
import os
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
# 连接手机
d = u2.connect()


class InstantAppsNotificationTest(unittest.TestCase):
    def open_instant_apps_notification_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Instant Apps Notification Test')
        d(text='Instant Apps Notification Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_instant_apps_notification_test()
        apk_path = os.path.join(os.path.join(rootPath, 'resource'), 'apk') + '\\CtsVerifierInstantApp.apk'
        os.system('adb install -r --instant ' + apk_path)
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/start_test_button").click()
        d.sleep(2)
        if not d(text="Sample Instant App for Testing").exists:
            self.mark_fail()
            raise AssertionError('测试失败,Instant App 打开失败,测试项：Instant_APPS_NOTIFICATION_TEST')
        d.open_notification()
        d.sleep(1)
        if not d(resourceId="android:id/app_name_text", text="Instant Apps").exists:
            d.swipe(0.5, 0.8, 0.5, 0.2)
            d.sleep(1)
        expand_button = d(resourceId="android:id/app_name_text", text="Instant Apps").sibling(
            resourceId="android:id/expand_button")
        if 'Expand' == expand_button.info.get('contentDescription'):
            expand_button.click()
            d.sleep(1)
        if not d(text="Manage").exists:
            d.swipe(0.5, 0.7, 0.5, 0.3)
            d.sleep(1)
        if not (d(text="GO TO BROWSER").exists or d(text="APP INFO").exists):
            self.mark_fail()
            raise AssertionError('测试失败,通知栏显示错误,测试项：Instant_APPS_NOTIFICATION_TEST')
        d(resourceId="android:id/action0", text="APP INFO").click()
        d.sleep(1)
        if not (d(resourceId="com.android.settings:id/launch").exists
                and d(resourceId="com.android.settings:id/clear_data").exists):
            self.mark_fail()
            raise AssertionError('测试失败,APP_INFO显示错误,测试项：Instant_APPS_NOTIFICATION_TEST')
        d.press('back')
        d.sleep(1)
        d.open_notification()
        d.sleep(1)
        if not d(resourceId="android:id/app_name_text", text="Instant Apps").exists:
            d.swipe(0.5, 0.8, 0.5, 0.2)
            d.sleep(1)
        expand_button = d(resourceId="android:id/app_name_text", text="Instant Apps").sibling(
            resourceId="android:id/expand_button")
        if 'Expand' == expand_button.info.get('contentDescription'):
            expand_button.click()
            d.sleep(2)
        if not d(text="Manage").exists:
            d.swipe(0.5, 0.7, 0.5, 0.3)
            d.sleep(2)
        if not (d(text="GO TO BROWSER").exists or d(text="APP INFO").exists):
            self.mark_fail()
            raise AssertionError('测试失败,通知栏显示错误,测试项：Instant_APPS_NOTIFICATION_TEST')
        d(resourceId="android:id/action0", text="GO TO BROWSER").click()
        d.sleep(3)
        if not 'com.android.chrome' == d.info.get('currentPackageName'):
            self.mark_fail()
            raise AssertionError('测试失败,打开浏览器失败,测试项：Instant_APPS_NOTIFICATION_TEST')
        d(resourceId="com.android.cts.verifier:id/pass_button").click()
        d.sleep(2)

    def mark_fail(self):
        self.open_instant_apps_notification_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
