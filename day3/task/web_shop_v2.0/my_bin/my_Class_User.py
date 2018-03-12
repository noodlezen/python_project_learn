#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    import __init__

import datetime

from my_bin import my_proces_text
from my_bin import my_API_mysql

RECORD_APELLATION_INIT = "初始记载"
RECORD_APELLATION_CURRT = "当前记载"
RECORD_APELLATION_LAST = "过去记载"


class Basic(object):
    def __init__(self, apellation, genre = None, created = None):
        self.apellation = apellation
        self.genre = genre
        if created == None: #如果缺省则视为创建，赋予当前时间。
            self.created = datetime.datetime.now()
        else:
            self.created = created

    def modify_apellation(self,new_apellation):
        self.apellation = new_apellation

#------------------------------
class Record(Basic, object):
    def __init__(self, apellation, genre, num, created = None):
        Basic.__init__(self, apellation, genre, created)
        self.num = num

#------------------------------
class Feature(Basic, object):
    def __init__(self, apellation, genre, created = None, modified_count = None):
        Basic.__init__(self, apellation, genre, created)
        self.record_array = []
        self.record_wordbook = {} #无序保存记载对象，key:记载名，value:记载对象
        self.record_count = 0
        if modified_count == None: #如果缺省则视为创建，赋予当前时间。
            self.modified_count = 0
        else:
            self.modified_count = modified_count

    def insert_record(self, apellation, genre, num):
        #调用my_proces_text模块规则检查，正确返回True,错误返回错误信息:
        rule_check = my_proces_text.check_record_rule(self.apellation, num)
        if rule_check == True:
            if self.apellation == '密码':
                num = my_proces_text.encrypt_str(num) #调用md5加密
            self.record = Record(apellation, genre, num)
            self.record_array.append(self.record)
            self.record_wordbook[apellation] = self.record #插入字典
            self.record_count += 1
            return True
        else:
            return rule_check

    def create_record(self, genre, num):
        result = Feature.insert_record(self, RECORD_APELLATION_INIT, genre, num)
        return result

    def update_record(self, genre, num):
        last_record = self.record_array[(self.record_count - 1)] #获取上一个记录对象。
        if last_record.apellation != RECORD_APELLATION_INIT:
            last_record.apellation = RECORD_APELLATION_LAST
        result = Feature.insert_record(self, RECORD_APELLATION_CURRT, genre, num)
        self.modified_count += 1
        return result

    def load_record(self, apellation, genre, num, created):
        self.record = Record(apellation, genre, num, created)
        self.record_array.append(self.record)
        self.record_wordbook[apellation] = self.record #插入字典
        self.record_count += 1

#------------------------------
class User(Basic, object):
    def __init__(self, apellation, genre = None, created = None):
        Basic.__init__(self, apellation, genre, created)
        self.feature_array = [] #按顺序保存特征对象
        self.feature_wordbook = {} #无序保存特征对象，key:特征名，value:特征对象
        self.feature_count = 0 #保存特征数量

    def create_feature(self, apellation, genre = None):
        self.feature = Feature(apellation, genre) #创建特征对象
        self.feature_array.append(self.feature) #插入数组
        self.feature_wordbook[apellation] = self.feature #插入字典
        self.feature_count += 1

    def load_feature(self,apellation, genre, created, modified_count):
        self.feature = Feature(apellation, genre, created, modified_count) #载入特征对象
        self.feature_array.append(self.feature) #插入数组
        self.feature_wordbook[apellation] = self.feature #插入字典
        self.feature_count += 1

    def locked(self, db_apellation, reason, duration, wrong_count): #时长单位分钟
        created = datetime.datetime.now()
        endtime = datetime.datetime.now() + datetime.timedelta(minutes = duration)
        sql_cmd = "INSERT INTO User_Locked (USER_APELLATION, REASON, WRONG_COUNT, CREATED, ENDTIME) VALUES ('%s', '%s', %d, '%s','%s')" % (
        self.apellation, reason, wrong_count, created, endtime)
        result = my_API_mysql.SQL(db_apellation, sql_cmd)
        return result

    def unlock(self, db_apellation):
        sql_cmd = "DELETE FROM User_Locked WHERE USER_APELLATION = '%s'" % self.apellation
        result = my_API_mysql.SQL(db_apellation, sql_cmd)
        return result

    def check_lock_state(self, db_apellation):
        sql_cmd = "SELECT ENDTIME FROM User_Locked WHERE USER_APELLATION = '%s'" % self.apellation #查询数据库
        result = my_API_mysql.SQL(db_apellation, sql_cmd)  # 以元组形式返回匹配到的结果。
        if len(result) != 0:
            endtime = result[0][0]
            nowtime = datetime.datetime.now()
            if nowtime > endtime:
                return True
            else:
                return (endtime - nowtime).total_seconds()
        else:
            return None #没有被锁定


def create_user(apellation, genre = None, created = None, db_apellation = None):
    #调用my_proces_text模块规则检查，正确返回True,错误返回错误信息:
    rule_check = my_proces_text.check_record_rule('用户名', apellation)
    if rule_check == True:
        sql_cmd = "SELECT USER_APELLATION FROM User WHERE USER_APELLATION = '%s'" % apellation #查询数据库
        result = my_API_mysql.SQL(db_apellation, sql_cmd)  # 以元组形式返回匹配到的结果。
        if len(result) == 0:
            ob_user = User(apellation, genre, created)
            return ob_user
        else:
            return '用户名已存在！'
    else:
        return rule_check


def login_user(apellation, genre = None, created = None, db_apellation = None):
    #调用my_proces_text模块规则检查，正确返回True,错误返回错误信息:
    rule_check = my_proces_text.check_record_rule('用户名', apellation)
    if rule_check == True:
        sql_cmd = "SELECT USER_APELLATION FROM User WHERE USER_APELLATION = '%s'" % apellation #查询数据库
        result = my_API_mysql.SQL(db_apellation, sql_cmd)  # 以元组形式返回匹配到的结果。
        if len(result) != 0:
            ob_user = User(apellation, genre, created)
            return ob_user
        else:
            return '用户名不存在！'
    else:
        return rule_check


# password_ob = ob_user.feature_wordbook['密码']
# print password_ob.apellation, password_ob.genre
# password_record_ob = password_ob.record_wordbook["初始记载"]
# print password_record_ob.apellation, password_record_ob.genre, password_record_ob.num

# ob = User('root', 'vip')
# ob.create_feature('用户名', 'personal')
# print ob.feature_array[0].apellation
# re = ob.feature.create_record('str', 'mass')
# print re
# print ob.feature_array[0].num_array[0].apellation
# ob.feature.update_record('str', 'w')
# print ob.feature_array[0].num_array[1].apellation
# ob.feature.update_record('str', '?')
# print ob.feature.modified_count
# ob.feature.update_record('str', 'm/w')
# print ob.feature.modified_count
# ob.create_feature('phone', 'personal')
# print ob.feature_array[1].apellation
# ob.feature.create_record('str', '888888')
# print ob.feature.num_array[0].apellation
# print ob.feature_array[0].num_array[2].apellation

# print ob.feature_array
# print ob.feature_array[0].record_array


# for i in ob.feature_array:
    # print i.record_count
    # for j in i.record_array:
        # print j.apellation, j.genre, j.num
    # print i.apellation, i.genre

