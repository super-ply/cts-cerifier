# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 17_1_6dof_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Sensors17.1 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class SixDoFTest(unittest.TestCase):
    def open_6dof_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='6DoF Test')
        d.sleep(1)
        d(text='6DoF Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_6dof_test()


if __name__ == '__main__':
    unittest.main()
