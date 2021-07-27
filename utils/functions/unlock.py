# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/4/21
# @File: unlock.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: 基于图像识别的图案解锁方案
# @update: Record important updates
# ---
import subprocess
import cv2
import numpy
import uiautomator2 as u2
from PIL import Image


def get_devices_list():
    """ 获取手机设备"""
    cmd = r'adb devices'
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    pr.wait()
    out = pr.stdout.readlines()  # out = pr.stdout.read().decode("UTF-8")
    devices = []
    for i in out[1:-1]:
        device = str(i).split("\\")[0].split("'")[-1]
        devices.append(device)
    return devices


def jiugongge_unlock():
    """
    九宫格解锁
    OpenCv模板匹配----多目标匹配
    """
    device = get_devices_list()
    if len(device) == 1:
        d = u2.connect(device[0])
        image = d.screenshot()                        # default format="pillow"
        image.save("screen_all.jpg")                  # 或'home.png'，目前只支持png 和 jpg格式的图像
        img = Image.open('screen_all.jpg')            # 打开一张图
        img_size = img.size                           # 图片尺寸
        h = img_size[1]                               # 图片高度
        print(h)
        w = img_size[0]                                     # 图片宽度
        region = img.crop((0, 0.5*h, w, h))                 # 开始截取
        region.save("screen_crop.jpg")                      # 保存图片
        coordinate = []                                     # 圆点坐标列表
        target = cv2.imread("screen_crop.jpg")              # 读取目标图片
        template = cv2.imread("template.jpg")               # 读取模板图片
        pic_height, pic_width = template.shape[:2]          # 获得模板图片的高宽尺寸
        # 执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
        # cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )                #归一化处理
        # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        cv2.rectangle(target, min_loc, (min_loc[0]+pic_width, min_loc[1]+pic_height), (0, 0, 225), 2)
        # 绘制矩形边框，将匹配区域标注出来
        # min_loc：矩形定点
        # (min_loc[0]+pic_width,min_loc[1]+pic_height)：矩形的宽高
        # (0,0,225)：矩形的边框颜色；2：矩形边框宽度
        asd_loc = (min_loc[0] + pic_width, min_loc[1] + pic_height)
        x_init = int((min_loc[0] + asd_loc[0])/2)
        y_init = int((min_loc[1] + asd_loc[1])/2 + 0.5 * h)
        coordinate.append((x_init, y_init))
        # 匹配值转换为字符串
        # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc
        # 对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc        # 初始化位置参数
        temp_loc = min_loc
        # 第一次筛选----规定匹配阈值，将满足阈值的从result中提取出来
        # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法设置匹配阈值为0.01
        threshold = 0.01
        loc = numpy.where(result < threshold)
        # 遍历提取出来的位置
        for other_loc in zip(*loc[::-1]):
            # 第二次筛选----将位置偏移小于5个像素的结果舍去
            if (temp_loc[0]+5 < other_loc[0]) or (temp_loc[1]+5 < other_loc[1]):
                temp_loc = other_loc
                you_loc = (other_loc[0] + pic_width, other_loc[1] + pic_height)
                # print(temp_loc)
                # print(you_loc)
                x = int((temp_loc[0] + you_loc[0])/2)
                y = int((temp_loc[1] + you_loc[1])/2 + 0.5 * h)
                coordinate.append((x, y))
                cv2.rectangle(target, other_loc, (other_loc[0]+pic_width, other_loc[1]+pic_height), (0, 0, 225), 2)
        # 显示结果
        # cv2.imshow(strText, target)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        print(coordinate)
        d.swipe_points([coordinate[0], coordinate[2], coordinate[-1]], 0.2)
    else:
        print('先不急着写!')




