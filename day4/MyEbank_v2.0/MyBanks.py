#!/usr/bin/env python
#_*_ coding:utf-8 _*_

''''''

# if __name__ == '__main__':
# import __init__

'''导入模块'''
import datetime
from MyAccount import *
from MyTools import *
from MyDateBase import *

'''定义常量'''

'''定义类'''

class MyBank(object):
    def __init__(self):
        self.__user_list = []  # 用户对象列表
        self.__user_dict = {}  # 用户对象字典，key:用户序号，value:用户对象
        self.text_rule = TextRule()
        self.text_proces = TextProces()
        self.mysql = MySQL()

    def __create_user(self, name, genre = None):
        self.__user = User(name, genre)
        self.__user_list.append(self.__user)  # 添加到用户列表
        self.__user_dict[name] = self.__user  # 添加到用户字典

    def __get_user_ob(self, name):
        self.__user = self.__user_dict[name]

    def __input_regist_info(self, meta):
        self.__tmp_var = raw_input("请输入%s:  " % meta)
        if meta == '密码':
            re_tmp_var = raw_input("请再次输入%s:  " % meta)
            if self.__tmp_var != re_tmp_var:
                return '密码不一致，请重新输入！'
        return self.text_rule.check_meta_value(meta, self.__tmp_var) #调用文本规则检测

    def __insert_regist_info(self):
        if self.mysql.insert_user_table(self.__user):
            user_id = self.mysql.load_user_id(self.__user.name)
            if user_id != False:
                for meta_ob in self.__user.meta_list:
                    if not self.mysql.insert_usermeta_table(user_id, meta_ob):
                        return False
                return True
            else:
                return False
        else:
            return False


    def regist_account(self, meta_list, meta_dict):
        for meta in meta_list:
            genre = meta_dict.get(meta)
            while(True):
                result = self.__input_regist_info(meta) #调用内部输入方法，返回规则检测信息
                if meta == '用户名':
                    if type(result) != str:
                        result = self.mysql.check_user_exist(self.__tmp_var) #调用重名检测，存在返回True,不存在返回False
                        if result:
                            result = '用户名已存在！'
                        else:
                            self.__create_user(self.__tmp_var)
                            break
                    print self.text_proces.color(result, 'red', 'l')
                else:
                    if type(result) != str:
                        if meta == '密码':
                            self.__tmp_var = self.text_proces.encrypt(self.__tmp_var)
                        self.__user.add_meta(genre[0], meta, self.__tmp_var, genre[1])
                        break
                    else:
                        print self.text_proces.color(result, 'red', 'l')
        print '显示信息'
        print '验证码'
        self.__insert_regist_info() #注册信息插入数据库


    def display_regist_info(self, name):
        self.__get_user_ob(name)
        tmp = '用户名:     ' + self.__user.name
        print self.text_proces.color(tmp, 'blue', 'l')
        for meta in self.__user.meta_list:
                if meta.name != "密码":
                    tmp = meta.genre + ' ' + meta.name + ':  ' + meta.value + ' ' + meta.types + ' ' + meta.status + ' ' + str(meta.modify)
                    print self.text_proces.color(tmp, 'blue', 'l')


'''定义函数'''


'''程序开始'''
# now_time = datetime.datetime.now()
# name = 'zneglei'
# genre = 'vip'
# print genre,type(genre)
# ob = TextProces()
# print ob.get_types(name)
# a = str(type(name))
# d = a.strip("<>").strip("type ").strip("'")
# mysql = MySQL()
# user_id = 2
# genre = '1'
# name = '2'
# value = '3'
# types = '4'
# status = '5'
# modify = 0
# created = datetime.datetime.now()
# sql_cmd = "INSERT INTO usermetas(user_id, umeta_genre, umeta_name, umeta_value, umeta_types, umeta_status, umeta_modify, umeta_created) VALUES (%d, '%s', '%s', '%s', '%s', '%s', %d, '%s')" % (user_id, genre, name, value, types, status, modify, created)
# sql_cmd = "INSERT INTO usermetas(user_id, umeta_name, umeta_value, umeta_created) VALUES (%d, '%s', '%s', '%s')" % (user_id, genre, name, value, types, status, modify, created)
# mysql.SQL(sql_cmd)
# mysql.create_usermeta_table()
# sql_cmd = "SELECT * FROM users WHERE user_login = '%s'" % name# 查询数据库
# res = mysql.SQL(sql_cmd)
# res = mysql.load_user_id('mp4102')
# print res
# print mysql.check_user_exist('mp4102')

# mysql.create_datebase('my_ebank')
# mysql.create_user_table()

# mysql.SQL("INSERT INTO users(user_login, user_genre, user_registered) VALUES ('%s','%s','%s')" % (name, genre, now_time))
# mysql.SQL("ALTER TABLE users DROP user_id")
# mysql.SQL("ALTER TABLE users ADD user_id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (user_id)")
# mysql.SQL("ALTER TABLE users AUTO_INCREMENT=2")
# mysql.SQL("INSERT INTO users(user_login) VALUES ('zl274')")

# text_rule = TextRule()
# result = text_rule.check_meta_value('用户名', 'mp4102')
# print result

# ss = 'sadasd'
# tools = TextProces()
# print MyTools.color(ss,'red','l')
# print tools.encrypt('asdas')
# print tools.color(ss,'red','l')
# db = MySQL()
# print db.SQL('SELECT VERSION()')[0][0]

# db.SQL("create table test (user_id integer primary key, username varchar(255) not null )")
# db.SQL("alter table test modify user_id integer auto_increment")
# db.SQL("INSERT INTO test(username) VALUES ('mp4102')")
