# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/7/19
# @File: test_sensors_17_2.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: 设计机械臂控制，进行尝试
# @update: Record important updates
# ---

import os
import socket
import json
import time
import unittest
import warnings
import uiautomator2 as u2
from utils.device_info_util.device_info import DeviceInfo


class AccelerometerMeasurementTests(unittest.TestCase):
    def setUp(self):
        support_device = 'HQ60CT3016'
        warnings.simplefilter('ignore', ResourceWarning)  # 屏蔽警报信息
        print("测试开始")
        print("获取手机设备信息！")
        self.device = DeviceInfo()
        print(support_device)
        self.devices = self.device.check_device()[0]
        self.devices.remove(support_device)
        self.test_device = self.devices[0]
        self.d = u2.connect(self.test_device)  # 连接待测设备
        self.d.unlock()
        print("解锁成功")


    def connect_et_controller(self, ip, port=8055):
        # 连接机器人
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, port))
            return True, sock
        except Exception as e:
            sock.close()
            return False, e

    def disconnect_et_controller(self, sock):
        if sock:
            sock.close()
            sock = None
        else:
            sock = None

    def send_cmd(self, sock, cmd, params=None, id=1):
        if not params:
            params = []
        else:
            params = json.dumps(params)
        sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id \":{2}}}".format(cmd, params, id) + "\n"
        try:
            sock.sendall(bytes(sendStr,"utf-8"))
            ret = sock.recv(1024)
            jdata = json.loads(str(ret, "utf-8"))
            if "result" in jdata.keys():
                return True, json.loads(jdata["result"]), jdata["id"]
            elif "error" in jdata.keys():
                return False, jdata["error"].jdata["id"]
            else:
                return False, None, None
        except Exception as e:
            print("fail:", str(e))
            return False, None, None

    def test_sensors_17_2(self):
        # adb 获取屏幕是否为自动亮度
        os.system("adb -s " + self.test_device + " shell settings get system screen_brightness_mode")
        # adb 更改屏幕为自动亮度
        os.system("adb -s " + self.test_device + " shell settings put system screen_brightness_mode 1")
        state = DeviceInfo().get_device_wifi_state(self.test_device)








