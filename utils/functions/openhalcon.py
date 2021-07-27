# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/4/25
# @File: openhalcon.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import cv2 as cv


class OpenHalcon:

    @staticmethod
    def threshold2(image, minvalue, maxvalue):
        """
        给定区间二值化
        :param image:原图
        :param minvalue:低阈值
        :param maxvalue:高阈值
        :return:灰度值位于低阈值和高阈值之间的区域 region
        """
        image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret1, thresh1 = cv.threshold(image_gray, minvalue, 255, cv.THRESH_BINARY)
        ret2, thresh2 = cv.threshold(image_gray, maxvalue, 255, cv.THRESH_BINARY)
        region = thresh1 - thresh2
        return region

    @staticmethod
    def connection2(region):
        """
        获取图像轮廓
        :param region:图像区域信息
        :return:轮廓 contours
        """
        contours, hierarchy = cv.findContours(region, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def select_shape_area(contours, minvalue, maxvalue):
        """
        获取面积处于给定区间内的轮廓
        :param contours: 轮廓集合
        :param minvalue: 低阈值
        :param maxvalue: 高阈值
        :return: 满足条件的轮廓集合
        """
        result_contours = []
        for i, contour in enumerate(contours):
            contour_area = cv.contourArea(contour)
            if minvalue < contour_area < maxvalue:
                result_contours.append(contour)
        return result_contours
