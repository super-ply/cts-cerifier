# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 14_2_recent_task_removal_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Other14.2 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import cv2 as cv
import uiautomator2 as u2

from utils.functions.compare import Compare
from utils.functions.vulcanadb import *

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
# 连接手机
d = u2.connect()


class RecentTaskRemovalTest(unittest.TestCase):
    def open_recent_task_removal_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Recent Task Removal Test')
        d(text='Recent Task Removal Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.do_test_setting()
        apk_path = os.path.join(os.path.join(rootPath, 'resource'), 'apk') + '\\CtsForceStopHelper.apk'
        os.system('adb install -r ' + apk_path)
        d.sleep(2)
        self.open_recent_task_removal_test()
        self.check_result()

    def check_result(self):
        temp_pass = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\t_pass.png')
        temp_fail = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\t_fail.png')
        pass_count = 0
        test_item1 = d(resourceId="com.android.cts.verifier:id/fs_test_app_install_status")
        flag = 0
        while pass_count < 1 and flag < 5:
            if Compare.compare_template(get_element_img(d, test_item1, 'index.png'), temp_pass):
                pass_count += 1
            elif Compare.compare_template(get_element_img(d, test_item1, 'index.png'), temp_fail):
                self.mark_fail()
                raise AssertionError('测试失败,测试项：RECENT_TASK_REMOVAL_TEST')
            else:
                d.sleep(5)
        d(resourceId="com.android.cts.verifier:id/fs_launch_test_app_button").click()
        d.sleep(5)
        if not d(text="Force stop helper app").exists:
            raise AssertionError('测试失败,测试项：RECENT_TASK_REMOVAL_TEST')
        d.press('back')
        d.sleep(3)
        flag = 0
        test_item2 = d(resourceId="com.android.cts.verifier:id/fs_test_app_launch_status")
        while flag < 5:
            if Compare.compare_template(get_element_img(d, test_item2, 'index.png'), temp_pass):
                break
            elif Compare.compare_template(get_element_img(d, test_item2, 'index.png'), temp_fail):
                self.mark_fail()
                raise AssertionError('测试失败,测试项：RECENT_TASK_REMOVAL_TEST')
            else:
                test_item2 = d(resourceId="com.android.cts.verifier:id/fs_test_app_launch_status")
                d.sleep(5)
                flag += 1
        d.press('recent')
        d.sleep(2)
        d.swipe(0.8, 0.5, 0.2, 0.5)
        d.sleep(2)
        flag = 0
        while flag < 5 and not d(resourceId="com.oppo.launcher:id/title_view", text="Force stop helper app").exists:
            d.swipe(0.2, 0.5, 0.8, 0.5)
            d.sleep(2)
            flag += 1
        if d(resourceId="com.oppo.launcher:id/title_view", text="Force stop helper app").exists:
            target_bounds = d(resourceId="com.oppo.launcher:id/title_view",
                              text="Force stop helper app").info.get('bounds')
            target_x = (target_bounds['left'] + target_bounds['right']) / 2
            d.swipe(target_x, 0.7, target_x, 0.3)
            d.sleep(2)
            d.press('back')
            d.sleep(2)
        flag = 0
        while flag < 5:
            if not d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
                d.sleep(5)
                flag += 1
            else:
                d(resourceId="com.android.cts.verifier:id/pass_button").click()
                d.sleep(2)
                break
        if d(resourceId="com.android.cts.verifier:id/fail_button").exists:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)

    def mark_fail(self):
        self.open_recent_task_removal_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)

    def do_test_setting(self):
        """打开DIsabel permission monitoring 开关"""
        # 打开开发者选项
        setting_package = 'com.android.settings'
        setting_activity = 'com.android.settings.Settings'
        d.app_start(package_name=setting_package, activity=setting_activity, stop=True)
        d.sleep(2)
        d(scrollable=True).scroll.to(text='About phone')
        d(text="About phone").click()
        d.sleep(2)
        d(resourceId="android:id/title", text="Version").click()
        d.sleep(2)
        for i in range(7):
            d(resourceId="android:id/title", text="Build number").click()
        d.app_start(package_name=setting_package, activity=setting_activity, stop=True)
        d.sleep(2)
        d(scrollable=True).scroll.to(text='Additional settings')
        d(text="Additional settings").click()
        d.sleep(2)
        d(scrollable=True).scroll.to(text='Developer options')
        d(text="Developer options").click()
        d.sleep(2)
        try:
            d(scrollable=True).scroll.to(text='Disable permission monitoring')
            d(text="Disable permission monitoring").click()
            d.sleep(2)
        except:
            return False
        widget_frames = d(resourceId='android:id/widget_frame')
        for widget_frame in widget_frames:
            if widget_frame.sibling(className='android.widget.RelativeLayout') \
                    .child(text='Disable permission monitoring').exists:
                switch_widget = widget_frame.child(resourceId='android:id/switch_widget')
                if not switch_widget.info.get('text') == 'On':
                    d(resourceId="android:id/title", text="Disable permission monitoring").click()
                    d.sleep(2)
                break


if __name__ == '__main__':
    unittest.main()
