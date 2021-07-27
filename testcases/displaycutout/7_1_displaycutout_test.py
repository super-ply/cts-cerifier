# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/3
# @File: 7_1_displaycutout_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS DisplayCutout7.1 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class DisplayCutoutTest(unittest.TestCase):
    def open_displaycutout_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='DisplayCutout Test')
        d(text='DisplayCutout Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_displaycutout_test()
        cut_out_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
        for cut_out in cut_out_list:
            d(text=cut_out).click()
            toast_info = d.toast.get_message(5, 3, 'Not Found Toast')
            msg_info = 'Button #' + cut_out + '  clicked'
            if not toast_info == msg_info:
                raise AssertionError('测试失败,Button #' + cut_out + ' Not Clicked! 测试项：DISPLAYCUTOUT_TEST')
            else:
                d.sleep(4)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
            raise AssertionError('测试失败,测试项：DISPLAYCUTOUT_TEST')


if __name__ == '__main__':
    unittest.main()
