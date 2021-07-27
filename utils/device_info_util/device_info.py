# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/3/25
# @File: search_device_info.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---
import os
from ..log_util.logcat import LogCat
from ..database_util.database_util import DataBase


class DeviceInfo(object):
    def __init__(self):
        self.log = LogCat()
        self.database = DataBase()
        self.sn = None
        self.device_all_info = None
        self.device_num = None

    def get_device_wifi_state(self, device):
        wifi_states = os.popen('adb -s ' + device + ' shell dumpsys wifi | findstr curState').read()
        states = str(wifi_states).split('\n')
        wifi_state = False
        for state in states:
            if 'ConnectModeState' in state:
                wifi_state = True
                break
            else:
                pass
        if wifi_state:
            print("wifi处于打开状态!")
            return 1
        else:
            print("wifi处于关闭状态!")
            return 0

    def set_device_wifi_on(self, device):
        os.system('adb -s ' + device + ' shell svc wifi enable')

    def set_device_wifi_off(self, device):
        os.system('adb -s ' + device + ' shell svc wifi disable')

    def get_device_bluetooth_state(self, device):
        bluetooth_state = os.popen('adb -s ' + device + ' shell settings get global bluetooth_on').read()
        return bluetooth_state

    def set_device_bluetooth_on(self, device):
        os.system('adb -s ' + device + ' shell settings put global bluetooth_on 1')

    def set_device_bluetooth_off(self, device):
        os.system('adb -s ' + device + ' shell settings put global bluetooth_on 0')

    def check_device(self):
        # 检测当前连接设备及状态
        i = 1
        device_serials = []
        order = 'adb devices'
        result = os.popen(order).readlines()
        # 防止adb启动信息干扰
        if 'daemon' in result[1]:
            self.device_all_info = result[3:-1]
        else:
            self.device_all_info = result[1:-1]
        self.device_num = len(self.device_all_info)
        if len(self.device_all_info) == 0:
            print('无设备信息，请检查设备是否插入！')
            self.log.console_out(level='warning', info='无设备信息，请检查设备是否插入！')
        else:
            print("连接设备数为" + str(self.device_num) + "台，现在进行连接设备状态检测！")
            for line in self.device_all_info:
                line.strip('\n')
                device_info = line
                print("获取到第" + str(i) + "台设备行信息：" + device_info)
                # self.log.console_out(level='info', info="获取到设备行信息：" + device_info)
                i += 1
                new_line = ' '.join(line.split())
                new_line_arr = new_line.split(' ')
                device_serial = new_line_arr[0]
                device_serials.append(device_serial)
                new_line_arr.remove(device_serial)
                device_status = ' '.join(new_line_arr)
                if device_status == 'device':
                    print('设备已连接')
                    # self.log.console_out(level='info', info='设备已连接')
                elif 'no permissions' in device_status:
                    print('未许可设备，请检查或切换至MTP选项')
                    # self.log.console_out(level='warning', info='未许可设备，请检查或切换至MTP选项')
                elif 'unauthorized' in device_status:
                    print('未授权！请授予USB调试权限')
                    # self.log.console_out(level='warning', info='未授权！请授予USB调试权限')
            print(device_serials)
            print(self.device_num)
        return device_serials, self.device_num

    def get_device_info(self):
        self.log.console_out('info', '获取手机基础信息')
        # 获取手机的序列号、IMEI、版本编号、样机配置(内存)
        sn = self.sn
        imei = 'unKnown'
        prop = 'unKnown'
        stage = 'unKnown'
        imei_query_sql = 'select ime_code,config_id,prototype_id from prototype_detail where sn_num=%s '
        res = self.database.exec(imei_query_sql, [sn])
        # print(res)
        if not res:
            self.log.console_out(level='info', info='未查询到与此样机相关的信息')
        else:
            imei = res[0][0].decode('utf8')
            config_id = res[0][1].decode('utf8')
            prototype_id = res[0][2].decode('utf8')
            prop_query_sql = 'select name from prototype_config where id =%s '
            prop = self.database.exec(prop_query_sql, [config_id])[0][0].decode('utf8')
            stage_query_sql = 'select stage from prototype where id =%s '
            stage = self.database.exec(stage_query_sql, [prototype_id])[0][0].decode('utf8')
        version = str(os.popen('adb -s ' + sn + ' shell getprop ro.build.version.ota').readlines()[0].strip())
        dut_detail = {'sn': sn, 'imei': imei, 'version': version, 'prop': prop, 'stage': stage}
        return dut_detail

    def get_product_id(self):
        product_id = None
        order = 'adb shell "getprop | grep ro.product.name"'
        response = os.popen(order).read()
        print(response)
        try:
            product_id = response.split(':')[1].strip().lstrip('[').rstrip(']')
            print(product_id)
        except Exception as e:
            print(e)
            self.log.console_out(level='info', info=e)
        return product_id


if __name__ == '__main__':
    DeviceInfo = DeviceInfo()
    DeviceInfo.check_device()
