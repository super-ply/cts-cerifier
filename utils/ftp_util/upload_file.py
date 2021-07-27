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
import os
import zipfile
from ftplib import FTP
from time import strftime, localtime


class UpLoadFile(object):
    def __init__(self):
        self.path = None

    def get_task_id(self, path):
        task_id = ''
        task_txt = open(path, 'r', encoding='utf-8')
        lines = task_txt.readlines()
        print(lines)
        for line in lines:
            if len(line) > 0 and ('taskid' in line):
                line = line.strip("\n")
                task_id = str(line).split('=')[1]
                print(task_id)
        task_txt.close()
        return task_id

    def zip_dir(self, dirpath, out_full_name):
        """
        压缩指定文件夹
        :param dirpath: 目标文件夹路径
        :param outFullName: 压缩文件保存路径+xxxx.zip
        :return: 无
        """
        zip = zipfile.ZipFile(out_full_name, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(dirpath):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(dirpath, '')

            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()

    def upload_file(self, local_path_whole, new_name_whole):
        time = strftime("%Y-%m-%d_%H:%M:%S", localtime())
        bufsize = 1024
        ftp = FTP()  # 打开调试级别2, 显示详细信息
        ftp.set_debuglevel(2)  # 服务器IP和端口
        ftp.connect("10.102.4.219", 21)
        ftp.login("ceshi", "ceshi123")  # 切换目录, 相对于ftp目录, 比如设置的ftp根目录为/vat/ftp, 那么pub就是/var/ftp下面的目录
        ftp.cwd("Logs")  # 查看目录下有哪些文件, 如果文件名已经存在, 那么再次上传同一个文件就会报错, 返回列表\
        task_id = self.get_task_id('.\\project')
        new_file = time + "_" + task_id
        ftp.mkd(new_file)
        ftp.cwd(new_file)  # 使用二进制的方式打开文件
        f = open(local_path_whole, 'rb')  # 上传文件, bufsize缓冲区大小
        ftp.storbinary("STOR " + new_name_whole, f, bufsize)
        f.close()  # 关闭调试模式
        ftp.set_debuglevel(0)  # 退出FTP连接
        ftp.quit()
        full_log_path = 'Logs/' + new_file + '/' + new_name_whole
        return full_log_path


if __name__ == '__main__':
    a = UpLoadFile()
    a.upload_file('.\\upload_file.py', 'test.txt')