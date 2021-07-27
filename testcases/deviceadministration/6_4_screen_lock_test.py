# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/3
# @File: 6_4_screen_lock_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS DeviceAdministration6.4 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class ScreenLockTest(unittest.TestCase):
    def open_screen_lock_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Screen Lock Test')
        d(text='Screen Lock Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_screen_lock_test()
        d(resourceId="com.android.cts.verifier:id/da_force_lock_button").click()
        d.sleep(1)
        d.swipe(0.5, 0.8, 0.5, 0.2)
        if d(text='Activate this device admin app').exists:
            d(text='Activate this device admin app').click()
            d.sleep(2)
        d.press('power')
        d.sleep(1)
        # 解锁屏幕
        d.swipe(0.5, 0.8, 0.5, 0.2)
        d.sleep(2)
        if d(text='It appears the screen was locked successfully!').exists:
            d(text='OK').click()
            d.sleep(1)
            if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
                d(resourceId="com.android.cts.verifier:id/pass_button").click()
                d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
            raise AssertionError('测试失败,测试项：DEVICE_ADMIN_UNINSTALL_TEST')


if __name__ == '__main__':
    unittest.main()
