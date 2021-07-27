# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/4/28
# @File: 11_3_2_progress_bar.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import time

import cv2 as cv
import uiautomator2 as u2
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
sys.path.append(rootPath)

from utils.functions.vulcanadb import *
from utils.functions.imageanalysis import *

device = u2.connect()

if __name__ == '__main__':
    # device.open_notification()
    # time.sleep(1)
    # if device(resourceId='com.android.systemui:id/clear_notifications').exists:
    #     device(resourceId='com.android.systemui:id/clear_notifications').click()
    #     time.sleep(2)
    # else:
    #     device.press('back')
    #     time.sleep(2)
    # device(text='REQUEST BUGREPORT').click()
    # time.sleep(2)
    # device.open_notification()
    # time.sleep(1)
    progress_bar = device(resourceId="android:id/progress")
    element_title = progress_bar.sibling(resourceId='android:id/title')
    if not element_title.exists or element_title.info.get('text') != 'Taking bug report…':
        raise AssertionError('不存在title为Taking bugreport ...的通知！')
    pre_progress_images = []
    for i in range(3):
        pre_progress_img = get_element_img(device, progress_bar, '1.png')
        cv.imwrite('1-' + str(i + 1) + '.png', pre_progress_img)
        pre_progress_images.append(pre_progress_img)
        time.sleep(1)
    img_starts = []
    for cv_img in pre_progress_images:
        img_starts.append(get_image_left_start(cv_img))
    print(img_starts)
    if img_starts[0] == img_starts[1] == img_starts[2]:
        raise AssertionError('进度条是静止的！')
    print('进度条是运动的!')
