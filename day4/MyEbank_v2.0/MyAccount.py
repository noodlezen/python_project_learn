#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''类的集成模块'''

# if __name__ == '__main__':
# import __init__

'''导入模块'''

import datetime

'''定义常量'''

'''定义类'''


class Basic(object):
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre
        self.created = datetime.datetime.now()

    def update_created(self, created):
        self.created = created


class Meta(Basic, object):
    def __init__(self, genre, name, value, types, status, modify):
        Basic.__init__(self, name, genre)
        self.value = value
        self.types = types
        self.status = status
        self.modify = modify

class User(Basic, object):
    def __init__(self, name, genre):
        Basic.__init__(self, name, genre)
        self.meta_order = 0
        self.meta_list = []
        self.meta_dict = {}

    def add_meta(self, genre, name, value, types):
        self.meta_order += 1
        self.meta = Meta(genre, name, value, types, '初始值', 0)
        self.meta_list.append(self.meta)
        self.meta_dict[name] = self.meta


'''定义函数'''


'''程序开始'''
