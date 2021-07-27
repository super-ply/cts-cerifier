# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/9
# @File: 13_3_ca_cert_notification_on_boot_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Notifications13.3 自动化测试脚本
# @update: Record important updates
# ---
import os
import time
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class CACertNotificationOnBootTest(unittest.TestCase):
    def open_ca_cert_notification_on_boot_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='CA Cert Notification on Boot test')
        d(text='CA Cert Notification on Boot test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_ca_cert_notification_on_boot_test()
        if not self.check_ca_certificate():
            self.install_ca_certificate()
        self.remove_screen_lock()
        self.reboot()
        self.remove_certificate()

    def check_ca_certificate(self):
        d(resourceId="com.android.cts.verifier:id/check_creds").click()
        d.sleep(4)
        if not d(resourceId="com.android.settings:id/trusted_credential_subject_primary").exists:
            d.press('back')
            d.sleep(1)
            return False
        d.press('back')
        d.sleep(1)
        return True

    def install_ca_certificate(self):
        # 安装CA证书
        d(resourceId="com.android.cts.verifier:id/install").click()
        d.sleep(1)
        d(resourceId="android:id/title", text="Encryption & credentials").click()
        d.sleep(1)
        d(resourceId="android:id/title", text="Install a certificate").click()
        d.sleep(1)
        d(resourceId="android:id/title", text="CA certificate").click()
        d.sleep(1)
        d(text="Install anyway").click()
        d.sleep(1)
        if not d(resourceId="android:id/title", text="myCA.cer").exists:
            d.swipe(0.5, 0.7, 0.5, 0.3)
            d.sleep(2)
        if not d(resourceId="android:id/title", text="myCA.cer").exists:
            d.swipe(0.5, 0.7, 0.5, 0.3)
            d.sleep(2)
        if not d(resourceId="android:id/title", text="myCA.cer").exists:
            self.mark_fail()
            raise AssertionError('测试失败,未找到指定证书,测试项：CA_CERT_NOTIFICATION_ON_BOOT_TEST')
        d(resourceId="android:id/title", text="myCA.cer").click()
        d.sleep(1)
        toast_info = d.toast.get_message(10, 3, 'NONE')
        if not 'CA certificate installed' == toast_info:
            self.mark_fail()
            raise AssertionError('测试失败,证书安装失败,测试项：CA_CERT_NOTIFICATION_ON_BOOT_TEST')
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)

    def remove_screen_lock(self):
        d(resourceId="com.android.cts.verifier:id/remove_screen_lock").click()
        d.sleep(1)
        d(resourceId="android:id/title", text="None").click()
        d.sleep(1)

    def reboot(self):
        os.system('adb reboot')
        time.sleep(70)

    def remove_certificate(self):
        d.open_notification()
        d.sleep(2)
        if not d(text="Manage").exists:
            d.swipe(0.5, 0.7, 0.5, 0.3)
            d.sleep(2)
        if not d(resourceId="android:id/title", text="Certificate authority installed").exists:
            self.mark_fail()
            raise AssertionError('测试失败,未发现通知,测试项：CA_CERT_NOTIFICATION_ON_BOOT_TEST')
        d(resourceId="android:id/title", text="Certificate authority installed").click()
        d.sleep(1)
        d(resourceId="android:id/button1").click()
        d.sleep(4)
        if not d(resourceId="com.android.settings:id/alertTitle", text="Security certificate").exists:
            self.mark_fail()
            raise AssertionError('测试失败,无证书详情,测试项：CA_CERT_NOTIFICATION_ON_BOOT_TEST')
        d(resourceId="android:id/button2", text="REMOVE").click()
        d.sleep(1)
        d(resourceId="android:id/button1", text="OK").click()
        d.sleep(1)
        d.open_notification()
        if not d(text="Manage").exists:
            d.swipe(0.5, 0.7, 0.5, 0.3)
            d.sleep(2)
        if d(resourceId="android:id/title", text="Certificate authority installed").exists:
            self.mark_fail()
            raise AssertionError('测试失败,通知仍存在,测试项：CA_CERT_NOTIFICATION_ON_BOOT_TEST')
        self.mark_pass()

    def mark_pass(self):
        d.press("back")
        d.sleep(1)
        d.press("back")
        d.sleep(1)
        self.open_ca_cert_notification_on_boot_test()
        if d(resourceId="com.android.cts.verifier:id/pass_button").exists:
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)

    def mark_fail(self):
        self.open_ca_cert_notification_on_boot_test()
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        self.open_ca_cert_notification_on_boot_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
