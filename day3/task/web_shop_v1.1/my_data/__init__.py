#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    print 'my_data模块初始化文件不能直接运行！'
else:
    import sys
    import os

    __PWD = os.getcwd()
    __FATHER_PATH = os.path.abspath(os.path.dirname(__PWD)+os.path.sep+".")

    sys.path.append(__PWD)
    sys.path.append(__FATHER_PATH)

    print 'my_data模块初始化成功！'
