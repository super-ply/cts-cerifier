# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/2
# @File: 5_1_4_full_alarm_test.py
# @Author: Restrain
# @E-mail: qiangzhongzhi@huaqin.com
# @Desc: Android 11 CTS Clock5.1.4 自动化测试脚本
# @update: Record important updates
# ---
import unittest

import uiautomator2 as u2
from utils.functions.vulcanadb import *
from utils.functions.openhalcon import OpenHalcon as halcon

package = 'com.android.cts.verifier'
activity = 'com.android.cts.verifier.CtsVerifierActivity'
d = u2.connect()


class FullAlarmTest(unittest.TestCase):

    def open_full_alarm_test(self):
        """
        打开测试项
        :return:
        """
        d.app_start(package_name=package, activity=activity, stop=True)
        d.sleep(3)
        if d(text="Location permission").exists:
            d.press('back')
            d.sleep(3)
        d(scrollable=True).scroll.to(text='Alarms and Timers Tests')
        d(text='Alarms and Timers Tests').click()
        d.sleep(2)
        if d(text='OK').exists:
            d(text='OK').click()
            d.sleep(1)
        d(resourceId="android:id/text1", text="Full Alarm Test").click()
        d.sleep(1)

    def test_main(self):
        self.open_full_alarm_test()
        d(resourceId="com.android.cts.verifier:id/buttons").click()
        d.sleep(2)
        # 清除弹窗
        d.swipe(0.5, 0.3, 0.5, 0.7)
        if not d(description="1:23 AM Create Alarm Test").exists:
            raise AssertionError('测试失败,未看到新建的闹钟,测试项：FULL_ALARM_TEST')
        alarm_name = d(description="Label Create Alarm Test").info.get('text')
        alarm_vibrate = d(resourceId="com.google.android.deskclock:id/vibrate_onoff").info.get('selected')
        alarm_ringtone = d(resourceId="com.google.android.deskclock:id/choose_ringtone").info.get('text')
        alarm_time = d(resourceId="com.google.android.deskclock:id/digital_clock").info.get('text').split(' ')[0]
        alarm_repeat = []
        repeat_frames = d(resourceId="com.google.android.deskclock:id/repeat_days").child(
            className='android.widget.FrameLayout').sibling(className='android.widget.FrameLayout')
        for i in range(7):
            repeat = repeat_frames[i].child(resourceId="com.google.android.deskclock:id/day_button_box")
            img = get_element_img(d, repeat, 'repeat_' + str(i + 1) + '.jpg')
            if halcon.select_color(img):
                alarm_repeat.append(i)
        print(alarm_name)
        print(alarm_vibrate)
        print(alarm_ringtone)
        print(alarm_time)
        print(alarm_repeat)
        # 相似度0.96->状态栏+表盘变化导致的误差
        if 'Create Alarm Test' == alarm_name \
                and not alarm_vibrate \
                and 'Silent' == alarm_ringtone \
                and '1:23' == alarm_time \
                and 1 == alarm_repeat[0] \
                and 3 == alarm_repeat[1]:
            d.press('back')
            d.sleep(2)
            d(resourceId="com.android.cts.verifier:id/pass_button").click()
            d.sleep(2)
        else:
            raise AssertionError('测试失败,测试项：FULL_ALARM_TEST')


if __name__ == '__main__':
    unittest.main()
