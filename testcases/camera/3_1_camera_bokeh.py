# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/1
# @File: 3_1_camera_bokeh.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
d = u2.connect()


class CameraBokeh(unittest.TestCase):

    def open_camera_bokeh(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Camera Bokeh')
        d(text='Camera Bokeh').click()
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_camera_bokeh()
        d(resourceId="com.android.cts.verifier:id/next_button").click()
        toast_info = d.toast.get_message(10, 3, 'Not Found Toast')
        if 'All Camera -1 tests are done.' == toast_info:
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
            raise AssertionError('测试失败,测试项：CAMERA_BOKEH')


if __name__ == '__main__':
    unittest.main()
