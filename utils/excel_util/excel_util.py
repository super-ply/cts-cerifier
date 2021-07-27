# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/3/15
# @File: upload_file.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: 日志上传至ftp服务器
# @update: Record important updates
# ---

import xlwt
from ..log_util.logcat import LogCat


class ExcelUtils:
    """写入Excel文件"""
    def __init__(self):
        self.log = LogCat()

    def create_excel(self, file_name, sheet_name):
        # 创建一个工作薄，编码默认是ASCII，为了支持中文要设置成UTF-8
        wb = xlwt.Workbook(encoding="utf-8")
        # 创建一个工作表
        sheet = wb.add_sheet(sheet_name)
        wb.save(file_name)
        self.log.console_out(level='info', info='新建成功！')

    def write_to_excel(self, info, filename, sheet_name='sheet1'):
        """重写excel"""
        # 1、创建工作簿
        work_book = xlwt.Workbook(encoding='utf-8')
        # 2、创建表单
        sheet = work_book.add_sheet(sheet_name)
        # 3、写表头，由于keys方法得到的是迭代器，不能直接使用len方法，需要转为列表。表头写在第一行，使用字典的键最为每一列属性名。
        head = list(info[0].keys())
        for i in range(len(head)):
            # write(行数，列数，内容)
            sheet.write(0, i, head[i])
        # 4、写入内容，从第二行开始，即行数坐标为1
        rows = 1
        # 获取每一行数据
        for i in info:
            # 写入每一列数据
            for j in range(len(head)):
                sheet.write(rows, j, i[head[j]])
            rows += 1
        # 保存工作簿
        work_book.save(filename)
        print("写入成功！")
        self.log.console_out(level='info', info='写入成功！')
