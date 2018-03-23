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

    def add_wrong(self, name, genre, toplimit, duration, user_id, meta_id):
        expiry_date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
        self.wrong = Wrong(name, genre, toplimit,
                           expiry_date, user_id, meta_id)

    def load_wrong(self, user_id=None, meta_id=None, wrong_id=None):
        wrong_dict = self.mysql.xload_userwrong(user_id, meta_id, wrong_id)
        if wrong_dict != False:
            wrong_id = wrong_dict['wrong_id']
            user_id = wrong_dict['user_id']
            meta_id = wrong_dict['meta_id']
            name = wrong_dict['wrong_name']
            genre = wrong_dict['wrong_genre']
            count = wrong_dict['wrong_count']
            toplimit = wrong_dict['wrong_toplimit']
            created = wrong_dict['wrong_created']
            expiry_date = wrong_dict['wrong_expiry_date']
            self.wrong = Wrong(name, genre, toplimit, expiry_date,
                               user_id, meta_id, wrong_id, count, created, wrong_dict)
            return True
        else:
            return False

    def delete_wrong(self, wrong_id):
        return self.mysql.delete_userwrong(wrong_id)


class Wrong(Basic, object):
    def __init__(self, name, genre, toplimit, expiry_date, user_id=0, meta_id=0, ID=None, count=1, created=None, wrong_dict=None):
        Basic.__init__(self, ID, name, genre, created)
        self.toplimit = toplimit
        self.expiry_date = expiry_date
        self.user_id = user_id
        self.meta_id = meta_id
        self.count = count
        self.wrong_dict = wrong_dict


    def check_duration(self):
        nowtime = datetime.datetime.now()
        return (self.expiry_date - nowtime).total_seconds() + 10 if nowtime <= self.expiry_date else False

    def check_count(self):
        return (self.toplimit - self.count) if self.count <= self.toplimit else False

    def modify_count(self, count):
        self.count = count
        self.wrong_dict['wrong_count'] = self.count

    def modify_name(self, name):
        self.name = name
        self.wrong_dict['wrong_name'] = self.name

    def insert_datebase(self):
        return self.mysql.insert_userwrong_table(self.user_id, self.meta_id, self.name, self.genre, self.count, self.toplimit, self.created, self.expiry_date)

    # def update_datebase_s(self, keys, keys_value):
        # return self.mysql.update_single('userwrong', keys, keys_value, 'wrong_id' , self.ID)

    def update_datebase(self):
        update_conut = 0
        res_dict = self.mysql.xload_userwrong(wrong_id=self.ID)
        for keys in res_dict.iterkeys():
            if res_dict[keys] != self.wrong_dict[keys]:
                self.mysql.update_single(
                    'userwrong', keys, self.wrong_dict[keys], 'wrong_id', self.ID)
                update_conut += 1
        return update_conut


class Meta(Basic, object):
    def __init__(self, name, genre, value, types, user_id=0, ID=None, modify=0, created=None, meta_dict=None):
        Basic.__init__(self, ID, name, genre, created)
        self.value = value
        self.types = types
        self.user_id = user_id
        self.modify = modify
        self.meta_dict = meta_dict

    def add_wrong(self, name, genre, toplimit, duration):
        Basic.add_wrong(self, name, genre, toplimit,
                        duration, self.user_id, self.ID)

    def load_wrong(self, wrong_id=None):
        return Basic.load_wrong(self, self.user_id, self.ID, wrong_id)

    def delete_wrong(self):
        self.mysql.delete_userwrong(self.wrong.ID)
        delattr(self, 'wrong')


    def get_id(self, user_id):
        self.ID = self.mysql.load_usermeta_id(user_id, self.name)
        return self.ID

    def cmp_value(self, meta_ob):
        return True if self.value == meta_ob.value else False

    def insert_datebase(self, user_id=None):
        user_id = self.user_id if user_id == None else user_id
        return self.mysql.insert_usermeta_table(user_id, self.name, self.genre, self.value, self.types, self.modify, self.created)

    def update_datebase(self):
        update_conut = 0
        res_dict = self.mysql.xload_usermeta(meta_id=self.ID)
        for keys in res_dict.iterkeys():
            if res_dict[keys] != self.meta_dict[keys]:
                self.mysql.update_single(
                    'usermeta', keys, self.meta_dict[keys], 'meta_id', self.ID)
                update_conut += 1
        return update_conut


class User(Basic, object):
    def __init__(self, name, genre, ID=None, status=0, created=None, user_dict=None):
        Basic.__init__(self, ID, name, genre, created)
        self.status = status
        self.user_dict = user_dict
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
        meta_dict = self.mysql.xload_usermeta(self.ID, meta_name)
        if meta_dict != False:
            meta_id = meta_dict['meta_id']
            user_id = meta_dict['user_id']
            name = meta_dict['meta_name']
            genre = meta_dict['meta_genre']
            value = meta_dict['meta_value']
            types = meta_dict['meta_types']
            modify = meta_dict['meta_modify']
            created = meta_dict['meta_created']
            self.meta = Meta(name, genre, value, types, user_id,
                             meta_id, modify, created, meta_dict)
            self.meta_list.append(self.meta)
            self.meta_dict[name] = self.meta  # 添加到用户字典
            return True
        else:
            return False

    # def add_wrong(self, name, genre, toplimit, duration, meta_id=0):
        # Basic.add_wrong(self, name, genre, toplimit,
                        # duration, self.ID, meta_id)

    # def load_wrong(self, meta_id=0, wrong_id=None):
        # return Basic.load_wrong(self, self.ID, meta_id, wrong_id)

    def lock(self, wrong_id):
        self.modify_status(wrong_id)

    def unlock(self):
        self.delete_wrong(self.wrong.ID)
        self.modify_status(0)

    def check_status(self):
        return True if self.status == 0 else self.status

    def modify_status(self, status):
        self.status = status
        self.user_dict['user_status'] = self.status

    def insert_datebase(self):
        return self.mysql.insert_user_table(self.name, self.genre, self.status, self.created)

    def update_datebase(self):
        update_conut = 0
        res_dict = self.mysql.xload_user(user_id=self.ID)
        for keys in res_dict.iterkeys():
            if res_dict[keys] != self.user_dict[keys]:
                self.mysql.update_single(
                    'users', keys, self.user_dict[keys], 'user_id', self.ID)
                update_conut += 1
        return update_conut


    # def lock(self, name, genre, duration):
        # self.add_wrong(name, genre, 1, duration)
        # self.wrong.insert_datebase()
        # self.load_wrong()
        # self.modify_status(self.wrong.ID)
'''定义函数'''
'''程序开始'''
