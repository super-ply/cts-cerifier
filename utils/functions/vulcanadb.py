# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/4/22
# @File: vulcanadb.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Phone UI工具类
# @update: Record important updates
# ---
import os
import subprocess

import cv2


def get_compare_element(device, element1_resource_id, element2_resource_id, img_name):
    """
    获取同一界面下两个控件对应的图像
    :param device UI设备
    :param element1_resource_id: 第一个控件的id
    :param element2_resource_id: 第二个控件的id
    :param img_name: 当前界面截图命名
    :return: (第一个控件的图像，第二个控件的图像)
    """
    preview = device(resourceId=element1_resource_id)
    res = device(resourceId=element2_resource_id)
    preview_bounds = preview.bounds()
    res_bounds = res.bounds()
    take_screen_shot(device, img_name)
    img = cv2.imread(img_name)
    img_pre = img[preview_bounds[1]:preview_bounds[3], preview_bounds[0]:preview_bounds[2]]
    img_pre_width = int(img_pre.shape[1] / 2)
    img_res_center = int((res_bounds[0] + res_bounds[2]) / 2)
    img_res = img[res_bounds[1]:res_bounds[3], img_res_center - img_pre_width:img_res_center + img_pre_width]
    cv2.imwrite('1-1.png', img_pre)
    cv2.imwrite('1-2.png', img_res)
    return img_pre, img_res


def get_element_img_by_class_name(device, element_class_name, index, img_name):
    """
    获取当前界面下控件对应的图像
    :param index: 角标
    :param device UI设备
    :param element_class_name: 控件的class
    :param img_name: 当前界面截图命名
    :return: 控件的图像
    """
    target_element = device(className=element_class_name)[index]
    preview_bounds = target_element.bounds()
    # take_screen_shot(device, img_name)
    device.screenshot(img_name)
    img = cv2.imread(img_name)
    target_img = img[preview_bounds[1]:preview_bounds[3], preview_bounds[0]:preview_bounds[2]]
    return target_img


def get_element_img_by_resource_id(device, element_resource_id, img_name):
    """
    获取当前界面下控件对应的图像
    :param device UI设备
    :param element_resource_id: 控件的id
    :param img_name: 当前界面截图命名
    :return: 控件的图像
    """
    target_element = device(resourceId=element_resource_id)
    preview_bounds = target_element.bounds()
    # take_screen_shot(device, img_name)
    device.screenshot(img_name)
    img = cv2.imread(img_name)
    target_img = img[preview_bounds[1]:preview_bounds[3], preview_bounds[0]:preview_bounds[2]]
    return target_img


def get_element_img_by_xpath(device, element_xpath, img_name):
    """
    获取当前界面下控件对应的图像
    :param device UI设备
    :param element_xpath: 控件的xpath
    :param img_name: 当前界面截图命名
    :return: 控件的图像
    """
    # take_screen_shot(device, img_name)
    device.screenshot(img_name)
    target_element = device.xpath(element_xpath).info
    preview_bounds = []
    element_bounds = target_element.get('bounds').values()
    for element_bound in element_bounds:
        preview_bounds.append(element_bound)
    img = cv2.imread(img_name)
    target_img = img[preview_bounds[1]:preview_bounds[3], preview_bounds[0]:preview_bounds[2]]
    return target_img


def get_element_img_by_text(device, text, img_name):
    """
    获取当前界面下控件对应的图像
    :param device UI设备
    :param text: 控件的text
    :param img_name: 当前界面截图命名
    :return: 控件的图像
    """
    # take_screen_shot(device, img_name)
    device.screenshot(img_name)
    target_element = device(text=text)
    preview_bounds = target_element.bounds()
    img = cv2.imread(img_name)
    target_img = img[preview_bounds[1]:preview_bounds[3], preview_bounds[0]:preview_bounds[2]]
    return target_img


def get_element_img(device, ui_element, image_name):
    device.screenshot(image_name)
    element_bounds = ui_element.info.get('bounds')
    img = cv2.imread(image_name)
    target_img = img[element_bounds['top']:element_bounds['bottom'], element_bounds['left']:element_bounds['right']]
    return target_img


def take_screen_shot(device, path):
    """
    获取手机截图
    :param device UI设备
    :param path: 截图保存路径。例：1.png; D:\GoogleTA\CTS\1.png
    """
    png = "/data/local/tmp/screenshot.png"
    cmd = " ".join(['rm', png + ';', 'screencap -p', png])
    adb_cmd = 'adb -s ' + device.serial + ' shell "' + cmd + '"'
    os.system('adb start-server')
    # print('exec {' + adb_cmd + '}')
    if os.name != 'nt':
        mShell = True
    else:
        mShell = False
    subprocess.Popen(adb_cmd, shell=mShell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    pull_cmd = 'adb -s ' + device.serial + ' pull -p ' + png + ' ' + path
    os.system('adb start-server')
    # print('exec {' + pull_cmd + '}')
    if os.name != 'nt':
        mShell = True
    else:
        mShell = False
    subprocess.Popen(pull_cmd, shell=mShell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
