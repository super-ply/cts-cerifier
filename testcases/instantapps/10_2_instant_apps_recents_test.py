# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/9
# @File: 10_2_instant_apps_recents_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS InstantApps10.2 自动化测试脚本
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


class InstantAppsRecentsTest(unittest.TestCase):
    def open_instant_apps_recents_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Instant Apps Recents Test')
        d(text='Instant Apps Recents Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_instant_apps_recents_test()
        apk_path = os.path.join(os.path.join(rootPath, 'resource'), 'apk') + '\\CtsVerifierInstantApp.apk'
        os.system('adb install -r --instant ' + apk_path)
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/start_test_button").click()
        d.sleep(2)
        if not d(text="Sample Instant App for Testing").exists:
            self.mark_fail()
            raise AssertionError('测试失败,Instant App 打开失败,测试项：Instant_APPS_RECENTS_TEST')
        d.press('recent')
        d.sleep(1)
        if not d(resourceId="com.android.launcher3:id/snapshot").exists:
            self.mark_fail()
            raise AssertionError('测试失败,Recent App打开失败,测试项：Instant_APPS_RECENTS_TEST')
        d.click(0.5, 0.5)
        if not d(text="Sample Instant App for Testing").exists:
            self.mark_fail()
            raise AssertionError('测试失败,返回Instant APP失败,测试项：Instant_APPS_RECENTS_TEST')
        self.mark_pass()

    def mark_pass(self):
        d.app_start(package_name=package, activity=activity)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(resourceId="com.android.cts.verifier:id/pass_button").click()
        d.sleep(2)

    def mark_fail(self):
        self.open_instant_apps_recents_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
