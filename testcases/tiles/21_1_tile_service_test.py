# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/17
# @File: 21_1_tile_service_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Tiles21.1 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2
import cv2 as cv

from utils.functions.compare import Compare
from utils.functions.vulcanadb import *

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
# 连接手机
d = u2.connect()


class TileServiceTest(unittest.TestCase):
    def open_tile_service_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Tile Service Test')
        d.sleep(1)
        d(text='Tile Service Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_tile_service_test()
        self.check_result()

    def check_result(self):
        temp_pass = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\t_pass.png')
        temp_fail = cv.imread(os.path.join(os.path.join(rootPath, 'resource'), 'pic') + '\\t_fail.png')
        test_items = d(resourceId="com.android.cts.verifier:id/tiles_test_items").child(
            className='android.widget.RelativeLayout').sibling(className='android.widget.RelativeLayout')
        src = get_element_img(d, test_items[0], 'index.jpg')
        while not Compare.compare_template(src, temp_pass) and not Compare.compare_template(src, temp_fail):
            src = get_element_img(d, test_items[0], 'index.jpg')
            d.sleep(2)
        d.sleep(2)
        d.open_notification()
        d.sleep(1)
        d.swipe(0.5, 0.2, 0.5, 0.8)
        d.sleep(1)
        d(resourceId="android:id/edit").click()
        d.sleep(2)
        flag = 0
        while flag < 3:
            if d(resourceId="com.android.systemui:id/list_top") \
                    .child(resourceId="com.android.systemui:id/tile_label",
                           text="Tile Service for CTS Verifier").exists:
                self.mark_fail()
                raise AssertionError('测试失败,存在 Tile Service,测试项：TILE_SERVICE_TEST')
            d.swipe(0.8, 0.35, 0.2, 0.35)
            d.sleep(2)
            flag += 1
        d.press('back')
        d.sleep(2)
        d.press('back')
        d.sleep(2)
        d.press('back')
        d.sleep(2)
        d(resourceId='com.android.cts.verifier:id/tiles_action_pass')[0].click()
        d.sleep(2)
        d.open_notification()
        d.sleep(1)
        d.swipe(0.5, 0.2, 0.5, 0.8)
        d.sleep(1)
        d(resourceId="android:id/edit").click()
        d.sleep(2)
        flag = 0
        while flag < 10:
            if d(resourceId="com.android.systemui:id/list_bottom") \
                    .child(resourceId="com.android.systemui:id/tile_label",
                           text="Tile Service for CTS Verifier").exists:
                break
            d.swipe(0.8, 0.75, 0.2, 0.75)
            d.sleep(2)
            flag += 1
        if flag < 10:
            d(resourceId="com.android.systemui:id/tile_label", text="Tile Service for CTS Verifier") \
                .drag_to(d(resourceId="com.android.systemui:id/list_top").child(className='android.widget.Button')[0])
        else:
            self.mark_fail()
            raise AssertionError('测试失败,不存在 Tile Service,测试项：TILE_SERVICE_TEST')
        if not d(resourceId="com.android.systemui:id/list_top") \
                .child(resourceId="com.android.systemui:id/tile_label",
                       text="Tile Service for CTS Verifier").exists:
            self.mark_fail()
            raise AssertionError('测试失败,Tile Service未能添加至快捷设置栏,测试项：TILE_SERVICE_TEST')
        d.press('back')
        d.sleep(2)
        d.press('back')
        d.sleep(2)
        d.press('back')
        d.sleep(2)
        d(resourceId='com.android.cts.verifier:id/tiles_action_pass')[1].click()
        d.sleep(2)
        while not d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            for test_item in test_items:
                src = get_element_img(d, test_item, 'index.png')
                if Compare.compare_template(src, temp_fail):
                    self.mark_fail()
                    raise AssertionError('测试失败,测试项：TILE_SERVICE_TEST')
        d(resourceId="com.android.cts.verifier:id/pass_button").click()
        d.sleep(2)

    def mark_fail(self):
        self.open_tile_service_test()
        d(resourceId="com.android.cts.verifier:id/fail_button").click()
        d.sleep(2)


if __name__ == '__main__':
    unittest.main()
