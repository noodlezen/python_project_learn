#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    import __init__

import time

from data import mysql
from bin import format_str

RECORD_APELLATION_INIT = "初始记载"
RECORD_APELLATION_CURRT = "当前记载"
RECORD_APELLATION_LAST = "过去记载"


class Basic(object):
    def __init__(self, apellation, genre = None):
        self.apellation = apellation
        self.genre = genre
        self.created = time.time()

#------------------------------
class Record(Basic, object):
    def __init__(self, apellation, genre, num):
        Basic.__init__(self, apellation, genre)
        self.num = num

#------------------------------
class Feature(Basic, object):
    def __init__(self, apellation, genre):
        Basic.__init__(self, apellation, genre)
        self.record_array = []
        self.record_count = 0
        self.modified_count = 0

    def insert_record(self, apellation, genre, num):
        self.record = Record(apellation, genre, num)
        self.record_array.append(self.record)
        self.record_count += 1

    def create_record(self, genre, num):
        Feature.insert_record(self, RECORD_APELLATION_INIT, genre, num)

    def update_record(self, genre, num):
        last_record = self.record_array[(self.record_count - 1)]
        if last_record.apellation != RECORD_APELLATION_INIT:
            last_record.apellation = RECORD_APELLATION_LAST 
        Feature.insert_record(self, RECORD_APELLATION_CURRT, genre, num)
        self.modified_count += 1

#------------------------------
class User(Basic, object):
    def __init__(self, apellation, genre = None):
        Basic.__init__(self, apellation, genre)
        self.feature_array = []
        self.feature_count = 0

    def create_feature(self, apellation, genre):
        self.feature = Feature(apellation, genre)
        self.feature_array.append(self.feature)
        self.feature_count += 1

    def printf(self):
        tmp = self.apellation + '   ' + self.feature.apellation + '   ' + \
            self.feature.record.apellation + '   ' + self.feature.record.num
        print format_str.color(tmp, 'red', 'l')
        print self.apellation, self.genre, self.feature.apellation, self.feature.genre, self.feature.record.apellation, self.feature.record.genre, self.feature.record.num

    def input_db(self):
        p_table = 'list_1'
        p_num1 = self.apellation
        p_num2 = self.feature.apellation
        p_num3 = self.feature.record.apellation
        p_num4 = self.feature.record.num
        sql = "INSERT INTO %s VALUES ('%s','%s','%s','%s')" % (
            p_table, p_num1, p_num2, p_num3, p_num4)
        mysql.SQL('Web_Shop_User_DB', sql)

'''
ob = User('root', 'vip')
ob.create_feature('age', 'personal')
# print ob.feature_array[0].apellation
ob.feature.create_record('str', 'm')
# print ob.feature_array[0].num_array[0].apellation
ob.feature.update_record('str', 'w')
# print ob.feature_array[0].num_array[1].apellation
ob.feature.update_record('str', '?')
print ob.feature.modified_count
ob.feature.update_record('str', 'm/w')
print ob.feature.modified_count
ob.create_feature('phone', 'personal')
# print ob.feature_array[1].apellation
ob.feature.create_record('str', '888888')
# print ob.feature.num_array[0].apellation
# print ob.feature_array[0].num_array[2].apellation

print ob.feature_array
print ob.feature_array[0].record_array


for i in ob.feature_array:
    print i.record_count
    for j in i.record_array:
        print j.apellation, j.genre, j.num
    print i.apellation, i.genre
'''


def register_user():
    user_apellation = raw_input(format_str.color(
        'Plaes input User apellation:\n', 'green', 'l'))
    ob = User(user_apellation, 'vip')

    while(1):
        feature_apellation = raw_input(format_str.color(
            'Plaes input feature apellation:\n', 'blue', 'l'))
        num_apellation = raw_input(format_str.color(
            'Plaes input record apellation:\n', 'yellow', 'l'))
        num = raw_input(format_str.color('Plaes input Vol:\n', 'red', 'l'))

        ob.create_feature(feature_apellation, 'personal', 'str')
        ob.feature.create_record(num_apellation, 'ing')
        ob.feature.num.create_num(num)

        ob.printf()

        tmp = raw_input(format_str.color('Plaes check!   y/n?\n', 'red', 'f'))
        if tmp == 'y':
            print 'Updata in MySQL'
            ob.input_db()

        tmp = raw_input(format_str.color('Qiut?   y/n\n', 'red', 'l'))
        if tmp == 'y':
            break
