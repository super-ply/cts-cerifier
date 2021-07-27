# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/9
# @File: 13_6_notification_listener_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Notifications13.6 自动化测试脚本
# @update: Record important updates
# ---
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


class NotificationListenerTest(unittest.TestCase):
    def open_notification_listener_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Notification Listener Test')
        d(text='Notification Listener Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_notification_listener_test()
        self.check_result()

    def check_result(self):
        temp_pass = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\pass.png')
        temp_fail = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\fail.png')
        flag = 0
        test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
            .child(className='android.widget.RelativeLayout') \
            .sibling(className='android.widget.RelativeLayout')
        if test_items[0].child(resourceId='com.android.cts.verifier:id/nls_action_button',
                               text='LAUNCH SETTINGS').info.get('enabled'):
            test_items[0].child(resourceId='com.android.cts.verifier:id/nls_action_button',
                                text='LAUNCH SETTINGS').click()
            d.sleep(2)
            d(scrollable=True).scroll.to(text='CTS Verifier')
            d(text='CTS Verifier').click()
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
        set_hints = d(resourceId="com.android.cts.verifier:id/nls_instructions",
                      text="Check that the listener can set hints.")
        while flag < 10 and not set_hints.exists:
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            pass_count = 0
            for test_item in test_items:
                if pass_count <= 5 and Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_pass):
                    pass_count += 1
                elif Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
                elif pass_count >= 5:
                    break
            print(pass_count)
            if pass_count >= 5:
                d.swipe(0.5, 0.6, 0.5, 0.4)
                d.sleep(1)
                flag = 0
            else:
                flag += 1
            print(flag)
        d.swipe(0.5, 0.6, 0.5, 0.4)
        d.sleep(1)
        while flag < 10 and not Compare.compare_template(
                get_element_img(d, set_hints.sibling(resourceId='com.android.cts.verifier:id/nls_status'), 'index.png'),
                temp_pass):
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            for test_item in test_items:
                if Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_pass):
                    continue
                elif Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
            d.sleep(3)
            flag += 1
        d.sleep(3)
        block_linked_application = d(resourceId="com.android.cts.verifier:id/nls_instructions",
                                     text="Please block the linked application and return here.")
        block_linked_application.sibling(resourceId='com.android.cts.verifier:id/nls_action_button').click()
        d.sleep(2)
        recycle_views = d(resourceId="com.coloros.notificationmanager:id/recycler_view").child(
            className='android.widget.LinearLayout')
        print(len(recycle_views))
        for recycle_view in recycle_views:
            if recycle_view.child(className='android.widget.RelativeLayout').exists \
                    and recycle_view.child(className='android.widget.RelativeLayout').child(
                resourceId="android:id/title").exists:
                if recycle_view.child(className='android.widget.RelativeLayout').child(
                        resourceId="android:id/title").info.get('text') == 'Allow notifications':
                    allow_switch = recycle_view.child(resourceId="android:id/widget_frame").child(
                        resourceId="android:id/switch_widget")
                    if allow_switch.info.get('checked'):
                        allow_switch.click()
                        d.sleep(2)
        d.press('back')
        d.sleep(2)
        d.swipe(0.5, 0.6, 0.5, 0.4)
        d.sleep(1)
        while flag < 10 and not Compare.compare_template(get_element_img(d, block_linked_application.sibling(
                resourceId='com.android.cts.verifier:id/nls_status'), 'index.png'), temp_pass):
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            for test_item in test_items:
                if Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_pass):
                    continue
                elif Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
            flag += 1
        d.sleep(3)
        un_block_linked_application = d(resourceId="com.android.cts.verifier:id/nls_instructions",
                                        text="Please unblock the linked application and return here.")
        un_block_linked_application.sibling(resourceId='com.android.cts.verifier:id/nls_action_button').click()
        d.sleep(2)
        recycle_views = d(resourceId="com.coloros.notificationmanager:id/recycler_view").child(
            className='android.widget.LinearLayout')
        print(len(recycle_views))
        for recycle_view in recycle_views:
            if recycle_view.child(className='android.widget.RelativeLayout').exists \
                    and recycle_view.child(className='android.widget.RelativeLayout').child(
                resourceId="android:id/title").exists:
                if recycle_view.child(className='android.widget.RelativeLayout').child(
                        resourceId="android:id/title").info.get('text') == 'Allow notifications':
                    allow_switch = recycle_view.child(resourceId="android:id/widget_frame").child(
                        resourceId="android:id/switch_widget")
                    if not allow_switch.info.get('checked'):
                        allow_switch.click()
                        d.sleep(2)
        d.press('back')
        d.sleep(2)
        d.swipe(0.5, 0.6, 0.5, 0.4)
        d.sleep(1)
        while flag < 10 and not Compare.compare_template(get_element_img(d, un_block_linked_application.sibling(
                resourceId='com.android.cts.verifier:id/nls_status'), 'index.png'), temp_pass):
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            for test_item in test_items:
                if Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_pass):
                    continue
                elif Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
            flag += 1
        d.sleep(3)
        block_linked_notification_channel = d(resourceId="com.android.cts.verifier:id/nls_instructions",
                                              text="Please block the linked notification channel and return here.")
        block_linked_notification_channel.sibling(resourceId='com.android.cts.verifier:id/nls_action_button').click()
        d.sleep(2)
        recycle_views = d(resourceId="com.coloros.notificationmanager:id/recycler_view").child(
            className='android.widget.LinearLayout')
        for recycle_view in recycle_views:
            if recycle_view.child(className='android.widget.RelativeLayout').exists \
                    and recycle_view.child(className='android.widget.RelativeLayout').child(
                resourceId="android:id/title").exists:
                if recycle_view.child(className='android.widget.RelativeLayout').child(
                        resourceId="android:id/title").info.get('text') == 'Allow notifications':
                    allow_switch = recycle_view.child(resourceId="android:id/widget_frame").child(
                        resourceId="android:id/switch_widget")
                    if allow_switch.info.get('checked'):
                        allow_switch.click()
                        d.sleep(2)
        d.press('back')
        d.sleep(2)
        d.swipe(0.5, 0.6, 0.5, 0.4)
        d.sleep(1)
        while flag < 10 and not Compare.compare_template(get_element_img(d, block_linked_notification_channel.sibling(
                resourceId='com.android.cts.verifier:id/nls_status'), 'index.png'), temp_pass):
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            for test_item in test_items:
                if Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_pass):
                    continue
                elif Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
            flag += 1
        d.sleep(3)
        block_notification_channel_group = d(resourceId="com.android.cts.verifier:id/nls_instructions",
                                             text="Please block the linked notification channel group and return here.")
        block_notification_channel_group.sibling(resourceId='com.android.cts.verifier:id/nls_action_button').click()
        d.sleep(2)
        d.swipe(0.5, 0.8, 0.5, 0.2)
        d.sleep(2)
        recycle_views = d(resourceId="com.coloros.notificationmanager:id/recycler_view").child(
            className='android.widget.LinearLayout')
        for recycle_view in recycle_views:
            # TODO 需要适配
            if recycle_view.child(className='android.widget.RelativeLayout').exists \
                    and recycle_view.child(className='android.widget.RelativeLayout').child(
                resourceId="com.coloros.notificationmanager:id/title").exists:
                if recycle_view.child(className='android.widget.RelativeLayout').child(
                        resourceId="com.coloros.notificationmanager:id/title").info.get(
                    'text') == 'ReceiveChannelBlockNoticeTest':
                    allow_switch = recycle_view.child(
                        resourceId="com.coloros.notificationmanager:id/widget_frame").child(
                        resourceId="com.coloros.notificationmanager:id/switchWidget")
                    if allow_switch.info.get('checked'):
                        allow_switch.click()
                        d.sleep(2)
        d.press('back')
        d.sleep(2)
        d.swipe(0.5, 0.6, 0.5, 0.4)
        d.sleep(1)
        while flag < 10 and not Compare.compare_template(get_element_img(d, block_notification_channel_group.sibling(
                resourceId='com.android.cts.verifier:id/nls_status'), 'index.png'), temp_pass):
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            for test_item in test_items:
                if Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_pass):
                    continue
                elif Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
            flag += 1
        d.sleep(3)
        msg_extra = d(resourceId="com.android.cts.verifier:id/nls_instructions",
                      text="Check that Message extras Bundle was preserved.")
        while flag < 10 and not msg_extra.exists:
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            pass_count = 0
            for test_item in test_items:
                if pass_count <= 5 and Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_pass):
                    pass_count += 1
                elif Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
                elif pass_count >= 5:
                    break
            print(pass_count)
            if pass_count >= 5:
                d.swipe(0.5, 0.6, 0.5, 0.4)
                d.sleep(1)
                flag = 0
            else:
                flag += 1
            print(flag)
        for i in range(3):
            if not d(resourceId="com.android.cts.verifier:id/iva_action_button_fail").exists:
                d.swipe(0.5, 0.6, 0.5, 0.4)
                d.sleep(1)
        d.open_notification()
        d.sleep(2)
        if not d(resourceId="android:id/app_name_text", text="CTS Verifier").exists:
            raise AssertionError('测试失败')
        if not d(resourceId="android:id/app_name_text", text="CTS Verifier").sibling(
                resourceId='android:id/expand_button').info.get('contentDescription') == 'Collapse':
            d(resourceId="android:id/app_name_text", text="CTS Verifier").click()
            d.sleep(2)
        if not d(resourceId="android:id/message_name", text='Person A').exists \
                or not d(resourceId="android:id/title", text="Non-Person Notification").exists:
            raise AssertionError("测试失败，此设备不支持对话通知或不将其分组")
        person_a = d(resourceId="android:id/message_name", text='Person A').info.get('bounds')
        person_non = d(resourceId="android:id/title", text="Non-Person Notification").info.get('bounds')
        if not person_a.get('bottom') < person_non.get('top'):
            raise AssertionError('测试失败，顺序不符合预期')
        d.press('back')
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/iva_action_button_pass").click()
        d.sleep(2)
        d.swipe(0.5, 0.8, 0.5, 0.2)
        d.sleep(2)
        hints_set = d(resourceId="com.android.cts.verifier:id/nls_instructions",
                      text="Check that the listener can set hints.")
        while flag < 10 and not Compare.compare_template(get_element_img(d, hints_set.sibling(
                resourceId='com.android.cts.verifier:id/nls_status'), 'index.png'), temp_pass):
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            for test_item in test_items:
                if Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_pass):
                    continue
                elif Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
            flag += 1
        d.sleep(5)
        d(resourceId="com.android.cts.verifier:id/nls_action_button").click()
        d.sleep(2)
        d(resourceId="android:id/title", text="CTS Verifier").click()
        d.sleep(2)
        if d(resourceId="android:id/switch_widget").info.get('checked'):
            d(resourceId="android:id/switch_widget").click()
            d.sleep(2)
            d(resourceId="android:id/button1").click()
            d.sleep(2)
        d.press('back')
        d.sleep(2)
        d.press('back')
        d.sleep(2)
        while flag < 10 and not d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            test_items = d(resourceId="com.android.cts.verifier:id/nls_test_items") \
                .child(className='android.widget.RelativeLayout') \
                .sibling(className='android.widget.RelativeLayout')
            for test_item in test_items:
                if Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_pass):
                    continue
                elif Compare.compare_template(
                        get_element_img(d, test_item.child(resourceId='com.android.cts.verifier:id/nls_status'),
                                        'index.png'), temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败')
            flag += 1
        d.sleep(2)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)

    def mark_pass(self):
        d.press("back")
        d.sleep(1)
        d.press("back")
        d.sleep(1)
        self.open_notification_listener_test()
        if d(resourceId="com.android.cts.verifier:id/pass_button").exists:
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)

    def mark_fail(self):
        self.open_notification_listener_test()
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        self.open_notification_listener_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
