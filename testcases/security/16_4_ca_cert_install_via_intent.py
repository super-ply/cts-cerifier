# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 16_4_ca_cert_install_via_intent.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Security16.4 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class CACertInstallViaIntent(unittest.TestCase):
    def open_projection_widget_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='CA Cert install via intent')
        d(text='CA Cert install via intent').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_projection_widget_test()
        self.check_result()

    def check_result(self):
        d(resourceId="com.android.cts.verifier:id/run_test_button").click()
        d.sleep(2)
        if d(text="Can't install CA certificates").exists and \
                d(text="CA certificates can put your privacy at risk and must be installed in Settings").exists:
            d(text='CLOSE').click()
            d.sleep(2)
            toast_info = d.toast.get_message(10, 3)
            if 'The certificate is not installed.' == toast_info:
                d(resourceId="com.android.cts.verifier:id/pass_button").click()
                d.sleep(2)
            else:
                self.mark_fail()
        else:
            self.mark_fail()

    def mark_fail(self):
        self.open_projection_widget_test()
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        d.press('back')
        d.sleep(1)
        self.open_projection_widget_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
