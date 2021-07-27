# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/9
# @File: 10_3_view_delete_instant_apps_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS InstantApps10.3 自动化测试脚本
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


class ViewDeleteInstantAppsTest(unittest.TestCase):
    def open_view_delete_instant_apps_test(self):
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
        self.open_view_delete_instant_apps_test()
        apk_path = os.path.join(os.path.join(rootPath, 'resource'), 'apk') + '\\CtsVerifierInstantApp.apk'
        os.system('adb install -r --instant ' + apk_path)
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/start_test_button").click()
        d.sleep(2)
        if not d(text="Sample Instant App for Testing").exists:
            self.mark_fail()
            raise AssertionError('测试失败,Instant App 打开失败,测试项：Instant_APPS_RECENTS_TEST')
        setting_package = 'com.android.settings'
        setting_activity = 'com.android.settings.Settings'
        d.app_start(package_name=setting_package, activity=setting_activity, stop=True)
        d(scrollable=True).scroll.to(text='Apps & notifications')
        d(text='Apps & notifications').click()
        d.sleep(1)
        d(resourceId="com.android.settings:id/header_details").click()
        d.sleep(1)
        d(resourceId="com.android.settings:id/filter_spinner").click()
        d.sleep(1)
        if not d(resourceId="android:id/text1", text="Instant apps").exists:
            self.mark_fail()
            raise AssertionError('测试失败,无Instant App筛选项,测试项：VIEW_DELETE_INSTANT_APPS_TEST')
        d(resourceId="android:id/text1", text="Instant apps").click()
        d.sleep(1)
        if not ('Sample Instant App for Testing' == d(resourceId="android:id/title").info.get('text')
                and d(resourceId="android:id/summary").exists):
            self.mark_fail()
            raise AssertionError('测试失败,Instant APP筛选失败,测试项：VIEW_DELETE_INSTANT_APPS_TEST')
        d(resourceId="android:id/title").click()
        d.sleep(1)
        if not (d(resourceId="com.android.settings:id/launch").exists
                and d(resourceId="com.android.settings:id/clear_data").exists):
            self.mark_fail()
            raise AssertionError('测试失败,APP_INFO显示错误,测试项：VIEW_DELETE_INSTANT_APPS_TEST')
        if not d(text="Sample Instant App for Testing").exists:
            self.mark_fail()
            raise AssertionError('测试失败,返回Instant APP失败,测试项：VIEW_DELETE_INSTANT_APPS_TEST')
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
        self.open_view_delete_instant_apps_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
