# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 16_7_keyguard_password_verification.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Security16.7 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class KeyguardPasswordVerification(unittest.TestCase):
    def open_keyguard_password_verification(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Keyguard Password Verification')
        d.sleep(1)
        d(text='Keyguard Password Verification').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_keyguard_password_verification()
        self.check_result()

    def lock_and_unlock(self, pwd):
        d.press('power')
        d.sleep(2)
        d.press('power')
        d.sleep(2)
        d.swipe(0.5, 0.7, 0.5, 0.3)
        d.sleep(1)
        d(resourceId="com.android.systemui:id/securityEditText").set_text(pwd)
        d.sleep(1)
        # 点击完成
        d.click(0.85, 0.95)
        pass

    def check_result(self):
        d(resourceId="com.android.cts.verifier:id/lock_set_btn").click()
        d.sleep(2)
        if d(text='Enter password').exists or d(text='Re-enter your password').exists:
            # 已有密码
            d(resourceId="com.android.settings:id/password_entry").set_text('a1234')
            d.sleep(1)
            d(resourceId="com.android.settings:id/menu_next").click()
            d.sleep(2)
        d(resourceId="android:id/title", text="Password").click()
        d.sleep(2)
        d(resourceId="com.android.settings:id/password_entry").set_text('a12345')
        d.sleep(1)
        d(resourceId="com.android.settings:id/menu_next").click()
        d.sleep(2)
        d(resourceId="com.android.settings:id/password_entry").set_text('a12345')
        d.sleep(2)
        d(resourceId="com.android.settings:id/menu_next").click()
        d.sleep(3)
        self.lock_and_unlock('a12345')
        d.sleep(2)
        if not d(text="Keyguard Password Verification").exists:
            self.mark_fail('a1234')
            raise AssertionError('测试失败,设置密码失败,测试项：KEYGUARD_PASSWORD_VERIFICATION')
        d(resourceId="com.android.cts.verifier:id/lock_change_btn").click()
        d.sleep(2)
        d(resourceId="com.android.settings:id/password_entry").set_text('a12345')
        d.sleep(1)
        d(resourceId="com.android.settings:id/menu_next").click()
        d.sleep(2)
        d(resourceId="android:id/title", text="Password").click()
        d.sleep(2)
        d(resourceId="com.android.settings:id/password_entry").set_text('a1234')
        d.sleep(1)
        d(resourceId="com.android.settings:id/menu_next").click()
        d.sleep(2)
        d(resourceId="com.android.settings:id/password_entry").set_text('a1234')
        d.sleep(2)
        d(resourceId="com.android.settings:id/menu_next").click()
        d.sleep(3)
        self.lock_and_unlock('a1234')
        d.sleep(2)
        if not d(text="Keyguard Password Verification").exists:
            self.mark_fail('a12345')
            raise AssertionError('测试失败,更改密码失败,测试项：KEYGUARD_PASSWORD_VERIFICATION')
        d(resourceId="com.android.cts.verifier:id/pass_button").click()
        d.sleep(2)

    def mark_fail(self, pwd):
        self.lock_and_unlock(pwd)
        self.open_keyguard_password_verification()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
