# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 16_5_identity_credential_via_intent.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Security16.5 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class IdentityCredentialViaIntent(unittest.TestCase):
    def open_identity_credential_via_intent(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Identity Credential Authentication')
        d(text='Identity Credential Authentication').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.set_screen_lock()
        self.open_identity_credential_via_intent()
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
        d(resourceId="com.android.cts.verifier:id/sec_start_test_button").click()
        d.sleep(2)
        toast_info = d.toast.get_message(10, 3)
        if 'No Identity Credential support, test passed.' == toast_info:
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)

    def tearDown(self) -> None:
        setting_package = 'com.android.settings'
        setting_activity = 'com.android.settings.Settings'
        d.app_start(setting_package, setting_activity)
        d(scrollable=True).scroll.to(text='Security')
        d.sleep(1)
        d(text='Security').click()
        d.sleep(2)
        if 'Password' == d(resourceId="android:id/title", text="Screen Lock").sibling(
                resourceId="android:id/summary").info.get('text'):
            d(resourceId="android:id/title", text="Screen Lock").click()
            d.sleep(2)
            d(resourceId="com.android.settings:id/password_entry").set_text('a1234')
            d.sleep(2)
            d(resourceId="com.android.settings:id/menu_next").click()
            d.sleep(2)
            d(resourceId="android:id/title", text="None").click()
            d.sleep(2)
            d(resourceId="android:id/button1", text='Yes, remove').click()
            d.sleep(2)


if __name__ == '__main__':
    unittest.main()
