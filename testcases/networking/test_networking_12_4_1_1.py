# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/7/19
# @File: test_networking_12_4_1_1.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Networking_12_4_1_1 自动化测试脚本
# @update: Record important updates
# ---
import os
import unittest

import uiautomator2
import uiautomator2 as u2
from utils.conf_util.conf_read import ConfigReader

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
setting_package = 'com.android.settings'
setting_activity = 'com.coloros.settings.feature.homepage.ColorSettingsHomepageActivity'
config_reader = ConfigReader()
devices = config_reader.read_conf_to_dict('project.conf', 'device')
dut = devices.get('dut_serial_num')
sup = devices.get('sup_serial_num')
# 连接手机
d1 = u2.connect(dut)
d2 = u2.connect(sup)


class TestNetworkingGroup1(unittest.TestCase):
    def open_test_networking(self, d: uiautomator2.Device):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Wi-Fi Direct Test')
        d(text='Wi-Fi Direct Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)
        d(text='GO Negotiation Responder Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)
        d2.app_start(package_name=package, activity=activity, stop=True)
        if d2(text="Location permission").exists:
            d2.press('back')
            d2.sleep(3)
        d2(scrollable=True).scroll.to(text='Wi-Fi Direct Test')
        d2(text='Wi-Fi Direct Test').click()
        d2.sleep(2)
        if d2(text='OK').exists:
            d2(text='OK').click()
            d2.sleep(1)
        d2(text='GO Negotiation Requester Test').click()
        d2.sleep(2)
        if d2(text='OK').exists:
            d2(text='OK').click()
            d2.sleep(1)

    def test_main(self):
        self.do_setting(d1)
        self.open_test_networking(d1)
        self.check_result()

    def check_result(self):
        self.sub_check_result('Go negotiation test (push button)')
        self.sub_check_result('Go negotiation test (PIN)')
        d1(resourceId="com.android.cts.verifier:id/pass_button").click()
        d1.sleep(2)

    def sub_check_result(self, sub_test_name):
        dut_name = d1(resourceId="com.android.cts.verifier:id/p2p_my_device").info.get('text').split(':')[1].strip()
        d2(resourceId="android:id/text1", text=sub_test_name).click()
        d2.sleep(15)
        items = d2(resourceId="android:id/select_dialog_listview").child(resourceId='android:id/text1')
        for item in items:
            if item.info.get('text') == dut_name:
                d2(resourceId="android:id/text1", text=dut_name).click()
                d2.sleep(2)
                break
        d2.sleep(30)
        if d1(resourceId="android:id/button1").exists:
            d1(resourceId="android:id/button1").click()
            d1.sleep(2)
        d1.sleep(5)
        if not d2(text='Test passed successfully.').exists:
            d1(resourceId="com.android.cts.verifier:id/fail_button")
            d1.sleep(2)
            raise AssertionError('测试失败,测试结果不匹配')
        d2(resourceId="com.android.cts.verifier:id/pass_button").click()
        d2.sleep(2)

    def do_setting(self, d: uiautomator2.Device):
        d.app_start(setting_package, setting_activity, stop=True)
        d.sleep(2)
        d2(scrollable=True).scroll.to(text='Location')
        d2(text='Location').click()
        d2.sleep(2)
        recycle_views = d(resourceId="com.android.settings:id/recycler_view").child(
            className='android.widget.LinearLayout')
        for recycle_view in recycle_views:
            if recycle_view.child(className='android.widget.RelativeLayout').exists \
                    and recycle_view.child(className='android.widget.RelativeLayout'). \
                    child(resourceId="android:id/title").exists:
                if recycle_view.child(className='android.widget.RelativeLayout').child(
                        resourceId="android:id/title").info.get('text') == 'Location':
                    allow_switch = recycle_view.child(resourceId="android:id/widget_frame").child(
                        resourceId="android:id/switch_widget")
                    if not allow_switch.info.get('checked'):
                        allow_switch.click()
                        d.sleep(2)
        d.press('back')
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
