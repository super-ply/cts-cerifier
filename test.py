# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/7/15
# @File: test.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import uiautomator2 as u2
import os
import pytesseract

d = u2.connect('15c2470')
d.swipe(0.5, 0.6, 0.5, 0.4)
# im = d.screenshot("home.jpg")
# text=pytesseract.image_to_string(im.open('home.jpg'), lang='eng')
# print(text)

# result = d(resourceId='com.android.cts.verifier:id/pass_button').info['enabled']
# print(type(result))
# if result == 'True':
#     print("测试pass!")


# device = '15c2470'
# a = os.path.abspath(os.path.join(os.getcwd(), ".."))
