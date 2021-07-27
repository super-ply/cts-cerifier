# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/7/21
# @File: test.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import uiautomator2 as u2
import os
from PIL import Image
import pytesseract

d = u2.connect('15c2470')
# if d(className='android.widget.RelativeLayout')[1].child(text="Contacts").exist:
#     print("asd")
# a = d(text="Allow").info
# print(type(a['enabled']))
for i in range(3):
    d.press("back")

#
# apk_path = os.path.abspath(os.path.join(os.getcwd(), "../../..")) + "\\resource\\apk\\CtsPermissionApp.apk"  # 测试结果图片文件夹保存路径
# print(apk_path)
# os.system("adb -s 15c2470 install " + apk_path)