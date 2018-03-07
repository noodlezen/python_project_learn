#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    print 'my_bin模块初始化文件不能直接运行！'
else:
    import sys
    import os

    __PWD = os.getcwd()#获取当前路径。
    __FATHER_PATH = os.path.abspath(os.path.dirname(__PWD)+os.path.sep+".")#过去父路径。

    #添加模块索引路径：
    sys.path.append(__PWD)
    sys.path.append(__FATHER_PATH)

    print 'my_bin模块初始化成功！'
