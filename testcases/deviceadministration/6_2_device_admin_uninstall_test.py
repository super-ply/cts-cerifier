# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/3
# @File: 6_2_device_admin_uninstall_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS DeviceAdministration6.2 自动化测试脚本
# @update: Record important updates
# ---
import os
import unittest

import uiautomator2 as u2

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
# 连接手机
d = u2.connect()


class DeviceAdminUninstallTest(unittest.TestCase):
    def open_device_admin_uninstall_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Device Admin Uninstall Test')
        d(text='Device Admin Uninstall Test').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)

    def test_main(self):
        self.open_device_admin_uninstall_test()
        apk_path = os.path.join(os.path.join(rootPath, 'resource'), 'apk') + '\\CtsEmptyDeviceAdmin.apk'
        os.system('adb install -t -r ' + apk_path)
        d.sleep(2)
        d(resourceId="com.android.cts.verifier:id/enable_device_admin_button").click()
        d.sleep(1)
        d(scrollable=True).scroll.to(text='Activate this device admin app')
        d(text='Activate this device admin app').click()
        d.sleep(1)
        d(resourceId="com.android.cts.verifier:id/open_app_details_button").click()
        d.sleep(1)
        d(text='UNINSTALL').click()
        d.sleep(1)
        d(scrollable=True).scroll.to(text='Deactivate & uninstall')
        d(text='Deactivate & uninstall').click()
        d.sleep(3)
        if d(text='Do you want to uninstall this app?').exists:
            d(text='OK').click()
            d.sleep(1)
        else:
            raise AssertionError('测试失败,未出现弹窗,测试项：DEVICE_ADMIN_UNINSTALL_TEST')
        if d(resourceId="com.android.cts.verifier:id/pass_button").info.get('enabled'):
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            d(resourceId="com.android.cts.verifier:id/fail_button").click()
            d.sleep(2)
            raise AssertionError('测试失败,测试项：DEVICE_ADMIN_UNINSTALL_TEST')


if __name__ == '__main__':
    unittest.main()
