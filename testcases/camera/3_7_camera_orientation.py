# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/4/21
# @File: 3_7_camera_orientation.py
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

from utils.functions.imageanalysis import *
from utils.functions.vulcanadb import *

device = uiautomator2.connect()

if __name__ == '__main__':
    # CTS测试 3.7 Camera Orientation
    images = get_compare_element(device, 'com.android.cts.verifier:id/camera_view',
                                 'com.android.cts.verifier:id/format_view',
                                 '1.png')
    similarity_rate = get_similarity(images[0], images[1])
    print('Similarity: ' + str(similarity_rate))
