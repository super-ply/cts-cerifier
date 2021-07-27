# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/3
# @File: pic_util.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: logcat
# @update: Record important updates
# ---
import colorsys


class PicUtil(object):
    def __init__(self):
        self.dominant_color = None
        pass

    def get_dominant_color(self, image):
        # 分析图片，获取图片的RGB值
        max_score = 0.0001
        for count, (r, g, b) in image.getcolors(image.size[0] * image.size[1]):
            # 转为HSV标准
            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
            y = (y - 16.0) / (235 - 16)
            # 忽略高亮色
            if y > 0.9:
                continue
            score = (saturation + 0.1) * count
            if score > max_score:
                max_score = score
                self.dominant_color = (r, g, b)
        return self.dominant_color
