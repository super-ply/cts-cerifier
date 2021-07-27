# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/4/23
# @File: 6_1_device_admin_tapjacking_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
sys.path.append(rootPath)

import uiautomator2

from utils.functions.vulcanadb import *

from utils.functions.imageanalysis import *

device = uiautomator2.connect()
if __name__ == '__main__':
    """
    CTS测试 3.7 Camera Orientation
    """
    #   判断浮窗是否存在
    float_xpaths = []
    for i in range(3):
        xpath = '//android.widget.FrameLayout[' \
                + str(i + 1) \
                + ']/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]'
        if not device.xpath(xpath).exists:
            continue
        else:
            float_xpaths.append(xpath)
    float_xpath = ''
    if not float_xpaths:
        raise AssertionError('浮窗不存在')
    for xpath in float_xpaths:
        resource_id = device.xpath(xpath).info.get('resourceId')
        if 'android:id/content' == resource_id:
            float_xpath = xpath
            break
    if float_xpath == '':
        raise AssertionError('浮窗不存在')
    # 截取浮窗区域的图片
    float_img = get_element_img_by_xpath(device, float_xpath, 'index.png')
    cv2.imwrite('float.png', float_img)
    #   判断图片是否透明
    print(is_transparent(float_img))
    #   判断按钮是否存在
    button_id = 'com.android.settings:id/restricted_action'
    if not device(resourceId=button_id).exists():
        raise AssertionError('按钮不存在')
    #   截取按钮区域的图片
    button_std_img = get_element_img_by_resource_id(device, 'com.android.settings:id/cancel_button', 'button.png')
    cv2.imwrite('button-std.png', button_std_img)
    button_cur_img = get_element_img_by_resource_id(device, button_id, 'index.png')
    cv2.imwrite('button-cur.png', button_cur_img)
    #   判断按钮是否灰显
    print(is_button_dimmed(button_std_img, button_cur_img))
