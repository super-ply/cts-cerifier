# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/7/16
# @File: test_networking_12_5_2_4.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Networking_12_5_2_4 自动化测试脚本
# @update: Record important updates
# ---
import unittest
import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
vpn_ssid = 'HQ_HKZX'
vpn_pwd = 'huaqin2020'
# 连接手机
d = u2.connect()


class TestNetworkingSuggest4(unittest.TestCase):
    def open_test_networking(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Wi-Fi Test')
        d(text='Wi-Fi Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)
        d(text='Network suggestion connection failure.').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_test_networking()
        self.check_result()

    def check_result(self):
        d(resourceId="com.android.cts.verifier:id/wifi_ssid").set_text(vpn_ssid)
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/wifi_psk").set_text(vpn_pwd)
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/wifi_start_test_btn").click()
        d.sleep(1)
        d.press('back')  # 收起输入法
        for j in range(3):
            if d(text='Allow suggested Wi‑Fi networks?').exists and d(text='ALLOW').exists:
                break
            d.sleep(5)
        if d(text='ALLOW').exists:
            d(text='ALLOW').click()
            d.sleep(2)
        for i in range(6):
            if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
                break
            d.sleep(10)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)


if __name__ == '__main__':
    unittest.main()
