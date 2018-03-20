#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''类的集成模块'''

# if __name__ == '__main__':
# import __init__

'''导入模块'''

import datetime
from MyDateBase import *

'''定义常量'''

'''定义类'''


class Basic(object):
    def __init__(self, ID, name, genre, created):
        self.ID = ID
        self.name = name
        self.genre = genre
        self.created = datetime.datetime.now() if created == None else created
        self.mysql = MySQL()


class Wrong(Basic, object):
    def __init__(self, name, genre, toplimit, expiry_date, user_id = None, meta_id = None, ID = None, count = None, created = None):
        Basic.__init__(self, ID, name, genre, created)
        self.toplimit = toplimit
        self.expiry_date = expiry_date
        self.user_id = 0 if user_id == None else user_id
        self.meta_id = 0 if meta_id == None else meta_id
        self.count = 1 if count == None else count

    def add_count(self):
        self.count += 1

    def check_duration(self):
        nowtime = datetime.datetime.now()
        return (self.expiry_date - nowtime).total_seconds() if nowtime <= self.expiry_date else False

    def check_count(self):
        return (self.toplimit - self.count) if self.count <= self.toplimit else False

    def insert_datebase(self):
        return self.mysql.insert_userwrong_table(self.user_id, self.meta_id, self.name, self.genre, self.count, self.toplimit, self.created, self.expiry_date)


class Meta(Basic, object):
    def __init__(self, name, genre, value, types, user_id = None, ID = None, modify = None, created = None):
        Basic.__init__(self, ID, name, genre, created)
        self.value = value
        self.types = types
        self.user_id = 0 if user_id == None else user_id
        self.modify = 0 if modify == None else modify

    def add_wrong(self, name, genre, toplimit, duration):
        expiry_date = datetime.datetime.now() + datetime.timedelta(minutes = duration)
        self.wrong = Wrong(name, genre, toplimit, expiry_date, self.user_id, self.ID)

    def load_wrong(self):
        result = self.mysql.load_userwrong(self.user_id, self.ID)
        if result != False:
            wrong_id= result[0]
            user_id= result[1]
            meta_id= result[2]
            name = result[3].encode('utf-8')
            genre= result[4].encode('utf-8')
            count = result[5]
            toplimit = result[6]
            created = result[7]
            expiry_date = result[8]
            self.wrong = Wrong(name, genre, toplimit, expiry_date, user_id, meta_id, wrong_id, count, created)
            return True
        else:
            return False

    def delete_wrong(self):
        return self.mysql.delete_userwrong(self.wrong.ID)

    def get_id(self, user_id):
        self.ID = self.mysql.load_umeta_id(user_id, self.name)
        return self.ID

    def insert_datebase(self, user_id = None):
        user_id = self.user_id if user_id == None else user_id
        return self.mysql.insert_usermeta_table(user_id, self.name, self.genre, self.value, self.types, self.modify, self.created)

    def cmp_value(self, meta_ob):
        return True if self.value == meta_ob.value else False


class User(Basic, object):
    def __init__(self, name, genre, ID = None, status = None, created = None):
        Basic.__init__(self, ID, name, genre, created)
        self.status = 0 if status == None else status
        self.meta_list = []
        self.meta_dict = {}

    def get_id(self):
        self.ID = self.mysql.load_user_id(self.name)
        return self.ID

    def add_meta(self, name, value, types):
        self.meta = Meta(name, '初始值', value, types)
        self.meta_list.append(self.meta)
        self.meta_dict[name] = self.meta  # 添加到用户字典

    def load_meta(self, meta_name):
        result = self.mysql.load_usermeta(self.ID, meta_name)
        if result != False:
            meta_id = result[0]
            user_id = result[1]
            name = result[2].encode('utf-8')
            genre= result[3].encode('utf-8')
            value = result[4].encode('utf-8')
            types = result[5].encode('utf-8')
            modify = result[6]
            created = result[7]
            self.meta = Meta(name, genre, value, types, user_id, meta_id, modify, created)
            self.meta_list.append(self.meta)
            self.meta_dict[name] = self.meta  # 添加到用户字典
            return True
        else:
            return False


    def insert_datebase(self):
        return self.mysql.insert_user_table(self.name, self.genre, self.status, self.created)



'''定义函数'''
'''程序开始'''
