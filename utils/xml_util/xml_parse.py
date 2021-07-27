# -*- coding: utf-8 -*-
# ---
# @Institution: Automation,T&E,Turing,HQ
# @Time: 2021/3/12
# @File: xml_parse.py
# @Author: pengleiyang
# @E-mail: pengleiyang@huaqin.com
# @Desc: Function of this file
# @update: Record important updates
# ---

# coding:utf-8
import xml.etree.ElementTree as ET

"""
实现从xml文件中读取数据
"""
# 全局唯一标识
unique_id = 1


# 遍历所有的节点
def walkData(root_node, level, result_list):
    global unique_id
    temp_list = [unique_id, level, root_node.tag, root_node.attrib]
    result_list.append(temp_list)
    unique_id += 1

    # 遍历每个子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        walkData(child, level + 1, result_list)
    return


def getXmlData(file_name):
    level = 1  # 节点的深度从1开始
    result_list = []
    root = ET.parse(file_name).getroot()
    walkData(root, level, result_list)
    return result_list


if __name__ == '__main__':
    # 'd:\\fenlei2.xml'
    file_name = './test_result.xml'
    R = getXmlData(file_name)
    with open('test_result.txt', mode='a', encoding='utf-8') as f:
        for line in R:
            f.write(str(line))


# def read_xml():
#     # read xml
#     dom_tree = parse("./test_result.xml")
#     # 文档根元素
#     root_node = dom_tree.documentElement
#     print(root_node.nodeName)
#     # 所有结果
#     customers = root_node.getElementsByTagName("result")
#     for customer in customers:
#         if customer.hasAttribute("ID"):
#             print("ID:", customer.getAttribute("TestCase"))
#             # name 元素
#             name = customer.getElementsByTagName("Test")[0]
#             print(name.nodeName, ":", name.childNodes[0].data)
#             # phone 元素
#             phone = customer.getElementsByTagName("Module")[0]
#             print(phone.nodeName, ":", phone.childNodes[0].data)
#             # comments 元素
#             comments = customer.getElementsByTagName("total_tests")[0]
#             print(comments.nodeName, ":", comments.childNodes[0].data)
#
#
# def update_xml():
#     # update xml
#     dom_tree = parse("./test_result.xml")
#     # 文档根元素
#     root_node = dom_tree.documentElement
#
#     names = root_node.getElementsByTagName("result")
#     for name in names:
#         if name.childNodes[0].data == "Module":
#             # 获取到name节点的父节点
#             pn = name.parentNode
#             # 父节点的phone节点，其实也就是name的兄弟节点
#             phone = pn.getElementsByTagName("total_tests")[0]
#             # 更新phone的取值
#             phone.childNodes[0].data = 'pass'
#     with open('updated_customer.xml', 'w') as f:
#         # 缩进 - 换行 - 编码
#         dom_tree.writexml(f, addindent='  ', encoding='utf-8')
#
#
# if __name__ == '__main__':
#     read_xml()
