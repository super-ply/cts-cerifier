# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/5/6
# @File: 11_1_40_Enable_location.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import os
import sys
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
sys.path.append(rootPath)

import uiautomator2 as u2

d = u2.connect()
if __name__ == '__main__':
    d(text='GO').click()
    time.sleep(3)
    switch_status = d(resourceId="com.android.settings:id/switch_widget").info['checked']
    if switch_status:
        d(resourceId="com.android.settings:id/switch_widget").click()
        time.sleep(3)
    d(resourceId="com.android.settings:id/switch_widget").click()
    time.sleep(3)
    d.press('home')
    time.sleep(3)
    toast_info = d.toast.get_message(20, 3, 'Not Found Toast')
    print(toast_info + '\n')
    if 'CTS Verifier:' not in toast_info:
        raise AssertionError('Location 更新的对话框未出现')
    print('出现Location 更新的对话框')
