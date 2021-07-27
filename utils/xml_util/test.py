from xml.dom import minidom


# 读取xml文档的方法
def read_xml_test(filename):
    # 打开这个文档，用parse方法解析
    parse_xml = minidom.parse(filename)
    # 获取根节点
    root = parse_xml.documentElement
    # 得到根节点下面所有的element节点
    # 更多方法可以参考w2school的内容或者用dir(root)获取
    elements = root.getElementsByTagName('Module')
    # 遍历处理，elements是一个列表

    for element in elements:
        # 判断是否有id属性
        if element.hasAttribute('name'):
            # 不加上面的判断也可以，若找不到属性，则返回空
            print('module_name:', element.getAttribute('name'))
        if element.hasAttribute('pass'):
            pass

        # 遍历element的子节点
        # for node in element.childNodes:
        #     # 通过nodeName判断是否是文本
        #     if node.nodeName == 'name':
        #         # 用data属性获取文本内容
        #         text = node.data.replace('\n', '')
        #         # 这里的文本需要特殊处理一下，会有多余的'\n'
        #         print(u'\t文本：', text)
        #     else:
        #         # 输出节点名
        #         print('\t' + node.nodeName)
        #
        #         # 输出属性值，这里可以用getAttribute方法获取
        #         # 也可以遍历得到，这是一个字典
        #         for attr, attr_val in node.attributes.items():
        #             print('\t\t', attr, ':', attr_val)


if __name__ == '__main__':
    # read_xml_test('./test_result.xml')
    htmlf = open('./test_result.html', 'r', encoding="utf-8")
    htmlcont = htmlf.read()
    print(htmlcont)
