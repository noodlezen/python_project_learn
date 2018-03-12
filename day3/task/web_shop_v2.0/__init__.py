#!/usr/bin/env python
#_*_ coding:utf-8 _*_

__CUSTOM_LIB_PATH = '/home/noodlezen/python_project_learn/day3/task/web_shop'

import sys

if __name__ == '__main__':
    print 'init main run'
else:
    sys.path.append(__CUSTOM_LIB_PATH)
    print sys.path
    print 'init funal'


