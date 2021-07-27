# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 16_8_lock_bound_keys_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Security16.8 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class LockBoundKeysTest(unittest.TestCase):
    def open_lock_bound_keys_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Lock Bound Keys Test')
        d.sleep(1)
        d(text='Lock Bound Keys Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_lock_bound_keys_test()
        self.check_result()

    def set_screen_lock(self):
        setting_package = 'com.android.settings'
        setting_activity = 'com.android.settings.Settings'
        d.app_start(setting_package, setting_activity)
        d(scrollable=True).scroll.to(text='Security')
        d.sleep(1)
        d(text='Security').click()
        d.sleep(2)
        if 'None' == d(resourceId="android:id/title", text="Screen Lock").sibling(
                resourceId="android:id/summary").info.get('text'):
            d(resourceId="android:id/title", text="Screen Lock").click()
            d.sleep(2)
            d(resourceId="android:id/title", text="Password").click()
            d.sleep(2)
            d(resourceId="com.android.settings:id/password_entry").set_text('a1234')
            d.sleep(2)
            d(resourceId="com.android.settings:id/menu_next").click()
            d.sleep(2)
            d(resourceId="com.android.settings:id/password_entry").set_text('a1234')
            d.sleep(2)
            d(resourceId="com.android.settings:id/menu_next").click()
            d.sleep(2)

    def check_result(self):
        if not d(resourceId="com.android.cts.verifier:id/sec_start_test_button").info.get('enabled'):
            self.set_screen_lock()
        d(resourceId="com.android.cts.verifier:id/sec_start_test_button").click()
        d.sleep(10)
        d(resourceId="com.android.systemui:id/lockPassword").set_text('a1234')
        d.sleep(2)
        d(resourceId="com.android.systemui:id/confirm").click()
        toast_info = d.toast.get_message(10, 3)
        if not 'Test passed.' == toast_info:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
            raise AssertionError('测试失败,更改密码失败,测试项：KEYGUARD_PASSWORD_VERIFICATION')
        d(resourceId="com.android.cts.verifier:id/pass_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
