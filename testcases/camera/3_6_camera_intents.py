# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/1
# @File: 3_6_camera_intents.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class CameraIntentsTest(unittest.TestCase):

    def check_popup(self):
        popup = ['WHILE USING THE APP', 'START CAPTURE']
        for pop in popup:
            if d(text=pop).exists:
                d(text=pop).click()
                d.sleep(2)

    def open_location_permission(self):
        """
        开启位置权限
        :return:
        """
        d(resourceId="com.android.cts.verifier:id/settings_button").click()
        d.sleep(1)
        d(resourceId="android:id/title", text="App access to location").click()
        d.sleep(1)
        d(scrollable=True).scroll.to(resourceId="android:id/title", text="CTS Verifier")
        d.sleep(1)
        d(resourceId="android:id/title", text="CTS Verifier").click()
        d.sleep(1)
        d(resourceId="com.android.permissioncontroller:id/allow_foreground_only_radio_button").click()
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)

    def close_location_permission(self):
        """
        关闭位置权限
        :return:
        """
        d(resourceId="com.android.cts.verifier:id/settings_button").click()
        d.sleep(1)
        d(resourceId="android:id/title", text="App access to location").click()
        d.sleep(1)
        d(scrollable=True).scroll.to(resourceId="android:id/title", text="CTS Verifier")
        d.sleep(1)
        d(resourceId="android:id/title", text="CTS Verifier").click()
        d.sleep(1)
        d(resourceId="com.android.permissioncontroller:id/deny_radio_button").click()
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)

    def open_camera_intents(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Camera Intents')
        d(text='Camera Intents').click()
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def new_picture_external(self):
        """
        拍照测试项Ⅰ
        :return:
        """
        d(resourceId="com.android.cts.verifier:id/start_test_button").click()
        d.sleep(1)
        d.press('home')
        d.sleep(1)
        d(text="Camera").click()
        d.sleep(1)
        d(resourceId="com.android.camera2:id/mode_scroll_text", text="Capture").click()
        d.sleep(1)
        d.sleep(2)
        d(resourceId="com.android.camera2:id/shutter_button").click()
        d.sleep(3)
        d.press('home')
        d.sleep(1)
        d.app_start(package_name=package, activity=activity)
        d.sleep(3)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(1)
        else:
            self.open_location_permission()
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(1)
            raise AssertionError('测试失败,测试项：NEW_PICTURE_EXTERNAL')

    def new_video_external(self):
        """
        摄像测试项Ⅰ
        :return:
        """
        d(resourceId="com.android.cts.verifier:id/start_test_button").click()
        d.press('home')
        d(text="Camera").click()
        d.sleep(1)
        d(resourceId="com.android.camera2:id/mode_scroll_text", text="Video").click()
        d.sleep(1)
        d.sleep(2)
        d(resourceId="com.android.camera2:id/shutter_button").click()
        d.sleep(7)
        d(resourceId="com.android.camera2:id/shutter_button").click()
        d.sleep(2)
        d.press('home')
        d.app_start(package_name=package, activity=activity)
        d.sleep(3)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(1)
        else:
            self.open_location_permission()
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(1)
            raise AssertionError('测试失败,测试项：NEW_VIDEO_EXTERNAL')

    def new_picture_internal(self):
        """
        拍照测试项Ⅱ-1
        :return:
        """
        d(resourceId="com.android.cts.verifier:id/start_test_button").click()
        d.sleep(2)
        d(resourceId="com.android.camera2:id/shutter_button").click()
        d.sleep(2)
        d(resourceId="com.android.camera2:id/done_button").click()
        d.sleep(3)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(1)
        else:
            self.open_location_permission()
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(1)
            raise AssertionError('测试失败,测试项：NEW_PICTURE_INTERNAL')

    def new_picture_internal_secure(self):
        """
        拍照测试项Ⅱ-2
        :return:
        """
        d(resourceId="com.android.cts.verifier:id/start_test_button").click()
        d.sleep(2)
        d(resourceId="com.android.camera2:id/shutter_button").click()
        d.sleep(2)
        d(resourceId="com.android.camera2:id/done_button").click()
        d.sleep(3)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(1)
        else:
            self.open_location_permission()
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(1)
            raise AssertionError('测试失败,测试项：NEW_PICTURE_INTERNAL_SECURE')

    def new_video_internal(self):
        """
        摄像测试项Ⅱ
        :return:
        """
        d(resourceId="com.android.cts.verifier:id/start_test_button").click()
        d.sleep(2)
        d(resourceId="com.android.camera2:id/shutter_button").click()
        d.sleep(7)
        d(resourceId="com.android.camera2:id/shutter_button").click()
        d.sleep(2)
        d(resourceId="com.android.camera2:id/done_button").click()
        d.sleep(3)
        self.open_location_permission()
        d.sleep(3)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(3)
            d.press('back')
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(1)
            raise AssertionError('测试失败,测试项：NEW_VIDEO_INTERNAL')

    def test_main(self):
        self.open_camera_intents()
        self.close_location_permission()
        self.new_picture_external()
        self.new_video_external()
        self.new_picture_internal()
        self.new_picture_internal_secure()
        self.new_video_internal()


if __name__ == '__main__':
    unittest.main()
