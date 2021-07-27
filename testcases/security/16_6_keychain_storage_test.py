# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 16_6_keychain_storage_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Security16.6 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class KeyChainStorageTest(unittest.TestCase):
    def open_keychain_storage_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='KeyChain Storage Test')
        d(text='KeyChain Storage Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_keychain_storage_test()
        self.check_result()

    def get_title(self, element):
        msg = element.info.get('text')
        return str(msg).split('\n')[0].strip('\t')

    def check_result(self):
        d(resourceId="com.android.cts.verifier:id/action_next").click()
        d.sleep(2)
        if not 'Reading resources' == self.get_title(d(resourceId="com.android.cts.verifier:id/test_log")):
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
            raise AssertionError('测试失败,第一次点击next，预期结果有误,测试项：KEYCHAIN_STORAGE_TEST')
        d(resourceId="com.android.cts.verifier:id/action_next").click()
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/action_next").click()
        d.sleep(3)
        d(resourceId="android:id/text1", text="VPN & app user certificate").click()
        d.sleep(2)
        d(resourceId="com.android.certinstaller:id/bottom_sheet_edit_text").set_text('KeyChainStorageTest')
        d.sleep(2)
        d(resourceId="com.android.certinstaller:id/menu_save").click()
        toast_info = d.toast.get_message(10, 3)
        if not 'User certificate installed' == toast_info:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
        if not 'Requesting install of credentials' == self.get_title(
                d(resourceId="com.android.cts.verifier:id/test_log")):
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
            raise AssertionError('测试失败,预期结果有误,测试项：KEYCHAIN_STORAGE_TEST')
        d(resourceId="com.android.cts.verifier:id/action_next").click()
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/action_next").click()
        d.sleep(3)
        d(text='KeyChainStorageTest').click()
        d.sleep(2)
        d(resourceId="android:id/button1", text='ALLOW').click()
        d.sleep(2)
        if not 'Starting web server' == self.get_title(
                d(resourceId="com.android.cts.verifier:id/test_log")):
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
            raise AssertionError('测试失败,预期结果有误,测试项：KEYCHAIN_STORAGE_TEST')
        d(resourceId="com.android.cts.verifier:id/action_next").click()
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/action_next").click()
        d.sleep(3)
        d(scrollable=True).scroll.to(text='KeyChain Storage Test')
        d.sleep(1)
        d(text='Credential storage').click()
        d.sleep(2)
        d(text='Remove all user certificates').click()
        d.sleep(2)
        d(resourceId="android:id/button1", text='OK').click()
        d.sleep(2)
        d(resourceId="com.android.settings:id/password_entry").set_text('a8888888')
        d.sleep(2)
        d(resourceId="com.android.settings:id/menu_next").click()
        toast_info = d.toast.get_message(10, 3)
        d.press('back')
        d.sleep(2)
        d.press('back')
        d.sleep(2)
        if not 'Credential storage is erased.' == toast_info:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/pass_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
