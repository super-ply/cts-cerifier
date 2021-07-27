# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/4/22
# @File: imageanalysis.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: 图像处理工具类
# @update: Record important updates
# ---
import cv2
from .openhalcon import OpenHalcon as halcon


def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                     (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def get_similarity(img1, img2):
    # RGB每个通道的直方图相似度
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    shape = img1.shape
    size = (shape[0], shape[1])
    image1 = cv2.resize(img1, size)
    image2 = cv2.resize(img2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return str(sub_data).strip('[').strip(']')


def is_transparent(img):
    threshold = 3000
    bg_color = [245, 245, 245]
    # 去除黑框
    img_bin = halcon.threshold2(img, 0, 50)  # 二值化，获取轮廓
    contours = halcon.connection2(img_bin)  # 解除掩膜连接，得到轮廓的集合
    res_contours = halcon.select_shape_area(contours, 50, 99999)  # 在轮廓的集合中过滤出面积在60-99999之间的轮廓
    for i, contour in enumerate(res_contours):
        cv2.drawContours(img, res_contours, i, (255, 255, 255, 0), 12)  # 将轮廓填充为白色
    res_img = rm_bg(img, threshold, bg_color)
    if res_img.std() > 104:
        return True
    return False


def is_button_dimmed(std_img, cur_img):
    """
    判断按钮是否灰显
    :param std_img: 标准按钮图像
    :param cur_img: 待判断按钮图像
    :return: True/False
    """
    threshold = 3000
    bg_color = [245, 245, 245]
    std_img_bgra = rm_bg(std_img, threshold, bg_color)
    cur_img_bgra = rm_bg(cur_img, threshold, bg_color)
    std_img_bgra = cv2.cvtColor(std_img_bgra, cv2.COLOR_BGR2GRAY)
    cur_img_bgra = cv2.cvtColor(cur_img_bgra, cv2.COLOR_BGR2GRAY)
    std_min = 255
    cur_min = 255
    for i in range(std_img_bgra.shape[0]):
        for j in range(std_img_bgra.shape[1]):
            if std_img_bgra[i][j] < std_min:
                std_min = std_img_bgra[i][j]
    for i in range(cur_img_bgra.shape[0]):
        for j in range(cur_img_bgra.shape[1]):
            if cur_img_bgra[i][j] < cur_min:
                cur_min = cur_img_bgra[i][j]
    if std_min < cur_min:
        return True
    return False


def rm_bg(img, threshold, bg_color):
    """
    去除图像背景(仅限纯色背景)
    :param img: 图像
    :param threshold: 参考均方差
    :param bg_color: 背景颜色
    :return 去除背景后的图像
    """
    img_bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    h, w = img_bgra.shape[0:2]
    for i in range(h):
        for j in range(w):
            if calc_diff(img_bgra[i][j], bg_color) < threshold:
                # 若logo[i][j]为背景，将其颜色设为白色，且完全透明
                img_bgra[i][j][0] = 255
                img_bgra[i][j][1] = 255
                img_bgra[i][j][2] = 255
                img_bgra[i][j][3] = 0
    return img_bgra


def calc_diff(pixel, bg_color):
    """
    计算pixel与背景的离差平方和，作为当前像素点与背景相似程度的度量
    """
    return (pixel[0] - bg_color[0]) ** 2 + (pixel[1] - bg_color[1]) ** 2 + (pixel[2] - bg_color[2]) ** 2


def get_image_left_start(cv_image):
    threshold = 3000
    bg_color = [245, 245, 245]
    img_bin = halcon.threshold2(cv_image, 235, 255)
    regions = halcon.connection2(img_bin)
    res_contours = halcon.select_shape_area(regions, 20, 9999)
    for i, contour in enumerate(res_contours):
        cv2.drawContours(cv_image, res_contours, i, (255, 255, 255), 3)  # 将轮廓填充为白色
    img_gray = rm_bg(cv_image, threshold, bg_color)
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(0)
    size = img_gray.shape[0:2]
    start = 0
    for i in range(size[0]):
        for j in range(size[1]):
            if img_gray[i][j] != 255:
                start = j
                break
    return start
