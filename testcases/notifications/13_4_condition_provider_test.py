# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/9
# @File: 13_4_condition_provider_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Notifications13.4 自动化测试脚本
# @update: Record important updates
# ---
import os
import time
import unittest

import uiautomator2 as u2
import cv2 as cv
from utils.functions.vulcanadb import *
from utils.functions.compare import Compare

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class ConditionProviderTest(unittest.TestCase):
    def open_condition_provider_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Condition Provider test')
        d(text='Condition Provider test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        # self.do_test_setting()
        os.system('adb shell settings put global hidden_api_policy 1')
        d.sleep(2)
        os.system('adb reboot')
        time.sleep(80)
        d.press('home')
        d.sleep(1)
        d.swipe(0.5, 0.8, 0.8, 0.2)
        d.sleep(2)
        os.system('adb shell settings put global hidden_api_policy 1')
        d.sleep(2)
        self.open_condition_provider_test()
        self.check_result()

    #     TODO 手动测试未通过

    def check_result(self):
        temp_pass = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\t_pass.png')
        temp_fail = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\fail.png')
        test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
            .child(className='android.widget.RelativeLayout') \
            .sibling(className='android.widget.RelativeLayout')
        flag = 0
        if not Compare.compare_template(get_element_img(d, test_items[0], 'index.png'), temp_pass) \
                and test_items[0].child(resourceId='com.android.cts.verifier:id/nls_action_button',
                                        text='LAUNCH SETTINGS').info.get('enabled'):
            test_items[0].child(resourceId='com.android.cts.verifier:id/nls_action_button',
                                text='LAUNCH SETTINGS').click()
            d(text="CTS Verifier").click()
            d.sleep(2)
            if d(resourceId="android:id/switch_widget").info.get('text') == 'Off':
                d(resourceId="android:id/switch_widget").click()
                d.sleep(2)
                d(resourceId="android:id/button1", text='Allow').click()
                d.sleep(2)
            d.press('back')
            d.sleep(2)
            d.press('back')
            d.sleep(2)
        test_item_target = d(resourceId="com.android.cts.verifier:id/nls_instructions",
                             text="Retrieving Automatic Zen Rules")
        while flag < 10 and not Compare.compare_template(
                get_element_img(d, test_item_target.sibling(resourceId='com.android.cts.verifier:id/nls_status'),
                                'index.png'), temp_pass):
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            for test_item in test_items:
                if Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
            test_item_target = d(resourceId="com.android.cts.verifier:id/nls_instructions",
                                 text="Retrieving Automatic Zen Rules")
            d.sleep(10)
            flag += 1
        test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
            .child(className='android.widget.RelativeLayout') \
            .sibling(className='android.widget.RelativeLayout')
        for test_item in test_items:
            if Compare.compare_template(
                    get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                    'index.png'), temp_fail):
                self.mark_fail()
                raise AssertionError('测试失败')
        d.swipe(0.5, 0.5, 0.5, 0.2)
        d.sleep(5)
        d(resourceId="com.android.cts.verifier:id/nls_instructions",
          text="Click this button to launch the Automatic Zen Rule listing page in settings, "
               "and then return to this screen").sibling(text='LAUNCH SETTINGS').click()
        d.sleep(2)
        rule_shown = False
        if d(text="Schedules").exists:
            rule_shown = True
        d.sleep(2)
        d.press('back')
        d.sleep(2)
        test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
            .child(className='android.widget.RelativeLayout') \
            .sibling(className='android.widget.RelativeLayout')
        for test_item in test_items:
            if Compare.compare_template(
                    get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                    'index.png'), temp_fail):
                self.mark_fail()
                raise AssertionError('测试失败')
        d.swipe(0.5, 0.5, 0.5, 0.2)
        d.sleep(5)
        if rule_shown:
            d(resourceId="com.android.cts.verifier:id/nls_instructions", text="Was the automatic rule screen shown?") \
                .sibling(resourceId='com.android.cts.verifier:id/iva_action_button_pass').click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/nls_instructions", text="Was the automatic rule screen shown?") \
                .sibling(resourceId='com.android.cts.verifier:id/iva_action_button_fail').click()
            d.sleep(2)
            self.mark_fail()
            raise AssertionError('测试失败')
        d(resourceId="com.android.cts.verifier:id/nls_instructions", text="Please disable rule 123 and return here.") \
            .sibling(resourceId='com.android.cts.verifier:id/nls_action_button').click()
        d.sleep(2)
        if d(resourceId="android:id/title", text="123").sibling(resourceId="android:id/summary") \
                .info.get('text') == 'On':
            d(resourceId="android:id/title", text="123").click()
            d.sleep(2)
        d.press('back')
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/nls_instructions", text="Please enable rule 123 and return here.") \
            .sibling(resourceId='com.android.cts.verifier:id/nls_action_button').click()
        d.sleep(2)
        d(resourceId="android:id/title", text="123").click()
        d.sleep(2)
        d.press('back')
        d.sleep(5)
        test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
            .child(className='android.widget.RelativeLayout') \
            .sibling(className='android.widget.RelativeLayout')
        for test_item in test_items:
            if Compare.compare_template(
                    get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                    'index.png'), temp_fail):
                self.mark_fail()
                raise AssertionError('测试失败')
        d.swipe(0.5, 0.5, 0.5, 0.2)
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/nls_instructions", text="Please delete rule 123 and return here.") \
            .sibling(resourceId='com.android.cts.verifier:id/nls_action_button').click()
        d.sleep(2)
        d(description="More options,").click()
        d.sleep(2)
        d(resourceId="com.android.settings:id/popup_list_window_item_title").click()
        d.sleep(2)
        d(resourceId="android:id/text1", text="123").click()
        d.sleep(2)
        d(resourceId="android:id/button1").click()
        d.sleep(2)
        d.press('back')
        d.sleep(2)
        test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
            .child(className='android.widget.RelativeLayout') \
            .sibling(className='android.widget.RelativeLayout')
        for test_item in test_items:
            if Compare.compare_template(
                    get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                    'index.png'), temp_fail):
                self.mark_fail()
                raise AssertionError('测试失败')
        d.swipe(0.5, 0.7, 0.5, 0.3)
        d.sleep(2)
        if Compare.compare_template(
                get_element_img(d, d(resourceId="com.android.cts.verifier:id/nls_instructions",
                                     text="Check the service can be unsnoozed.")
                        .sibling(resourceId='com.android.cts.verifier:id/nls_status'), 'index.png'), temp_pass):
            d(resourceId="com.android.cts.verifier:id/nls_instructions",
              text='Please disable "CTS Verifier" under Do Not Disturb access and return here.') \
                .sibling(resourceId='com.android.cts.verifier:id/nls_action_button').click()
            d(scrollable=True).scroll.to(text='CTS Verifier')
            d(text='CTS Verifier').click()
            d.sleep(2)
            if d(resourceId="android:id/switch_widget").info.get('text') == 'On':
                d(resourceId="android:id/switch_widget").click()
                d.sleep(2)
                d(resourceId="android:id/button1", text='OK').click()
                d.sleep(2)
            d.press('back')
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
                break

    def mark_fail(self):
        self.open_condition_provider_test()
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
