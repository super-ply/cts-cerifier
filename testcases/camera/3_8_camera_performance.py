# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/1
# @File: 3_8_camera_performance.py
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


class CameraPerformance(unittest.TestCase):

    def open_camera_performance(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Camera Performance')
        d(text='Camera Performance').click()
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_camera_performance()
        titles = d(text='testSingleCapture').sibling(resourceId='android:id/text1')
        for title in titles:
            title.click()
            d.sleep(3)
            while d(text='Running CTS performance test case...').exists:
                d.sleep(5)
                d.click(0.5, 0.5)
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
            raise AssertionError('测试失败,测试项：CAMERA_PERFORMANCE')


if __name__ == '__main__':
    unittest.main()
