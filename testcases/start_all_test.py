# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/6/1
# @File: start_all_test.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: 启动程序
# @update: Record important updates
# ---

import os
import time
import unittest
import HTMLTestRunner



case_path = os.getcwd() + "\\managedprovisioning\\byodmanagedprovisioning\\"  # 测试结果图片文件夹保存路径


# 报告存放路径
report_path = os.path.join(os.getcwd(), 'report')
print(report_path)

if os.path.exists("report/"):
    print("报告文件夹已存在！")
else:
    os.makedirs("report/")

def all_case():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py", top_level_dir=None)
    print(discover)
    return discover


if __name__ == '__main__':
    # 1、获取当前时间，这样便于下面的使用。
    print(report_path)
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 2、html报告文件路径
    report_abspath = os.path.join(report_path, "result_"+now+".html")
    # 3、如果没有report_path，则创建此目录
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    # 4、打开一个文件，将result写入此file中
    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'cts_verifier自动化测试报告,测试结果如下：',
                                           description=u'用例执行情况：')
    # 5、调用add_case函数返回值
    runner.run(all_case())
    fp.close()
