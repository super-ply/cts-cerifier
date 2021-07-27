# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 18_1_streaming_video_quality_verifier.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Streaming18.1 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class StreamingVideoQualityVerifier(unittest.TestCase):
    def open_streaming_video_quality_verifier(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Streaming Video Quality Verifier')
        d.sleep(1)
        d(text='Streaming Video Quality Verifier').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.connect_wifi()
        self.open_streaming_video_quality_verifier()
        self.check_result()

    def check_result(self):
        d(resourceId="android:id/text1", text="MPEG4 SP Video, AAC Audio").click()
        d.sleep(12)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
        d(resourceId="android:id/text1", text="H264 Base Video, AAC Audio").click()
        d.sleep(12)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
        d.sleep(5)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)

    def connect_wifi(self):
        setting_package = 'com.android.settings'
        setting_activity = 'com.android.settings.Settings'
        d.app_start(setting_package, setting_activity)
        d(resourceId="android:id/title", text="Wi-Fi").click()
        d.sleep(2)
        d(scrollable=True).scroll.to(resourceId="android:id/title", text="HQ_HKZX")
        d.sleep(1)
        wifi_titles = d(resourceId='com.coloros.wirelesssettings:id/ll_title')
        target_wifi = wifi_titles
        for wifi_title in wifi_titles:
            if wifi_title.child(resourceId="android:id/title", text="HQ_HKZX").exists:
                target_wifi = wifi_title
                break
        if not target_wifi.sibling(resourceId="android:id/summary").exists:
            target_wifi.click()
            d.sleep(2)
            d(resourceId="android:id/input").set_text('huaqin2020')
            d.sleep(2)
            d(resourceId="com.coloros.wirelesssettings:id/menu_save").click()
            d.sleep(2)


if __name__ == '__main__':
    unittest.main()
