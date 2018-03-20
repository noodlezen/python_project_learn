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
        self.user_list = []  # 用户对象列表
        self.user_dict = {}  # 用户对象字典，key:用户序号，value:用户对象
        self.text_rule = TextRule()
        self.text_proces = TextProces()
        self.mysql = MySQL()

    def __create_user(self, name, genre = None):
        self.__user = User(name, genre) #创建零时用户对象

    def load_user(self, user_name):
        result = self.mysql.load_user(user_name)
        if result != False:
            user_id= result[0]
            name = result[1].encode('utf-8')
            genre= result[2].encode('utf-8')
            status = result[3]
            created = result[4]
            self.user = User(name, genre, user_id, status, created)
            self.user_list.append(self.user)  # 添加到用户列表
            self.user_dict[name] = self.user  # 添加到用户字典
            return True
        else:
            return False


    def delete_user(self, user_ob):
        self.user_list.remove(user_ob)
        self.user_dict.pop(user_ob.name)

    def __get_user_ob(self, name):
        self.__user = self.__user_dict[name]


    def __input_regist_info(self, meta):
        self.__tmp_var = raw_input("请输入%s:  " % meta)
        if meta == '用户密码':
            re_tmp_var = raw_input("请再次输入%s:  " % meta)
            if self.__tmp_var == re_tmp_var:
                result = self.text_rule.check_meta_value(meta, self.__tmp_var) #调用文本规则检测
                if result == True:
                    self.__tmp_var = self.text_proces.encrypt(self.__tmp_var) #给用户密码加密
                    return True
                else:
                    return result
            else:
                return '用户密码不一致，请重新输入！'
        return self.text_rule.check_meta_value(meta, self.__tmp_var) #调用文本规则检测

    def __input_login_info(self, meta):
        self.__tmp_var = raw_input("请输入%s:  " % meta)
        if meta == '用户密码':
            self.__tmp_var = self.text_proces.encrypt(self.__tmp_var) #给用户密码加密

    def __insert_regist_info(self):
        if self.__user.insert_datebase(): #插入数据库
            if self.__user.get_id() != False: #获得数据库ID
                for meta_ob in self.__user.meta_list:
                    if not meta_ob.insert_datebase(self.__user.ID): #插入数据库
                        return False
                return True
            else:
                return False
        else:
            return False

    def __display_regist_info(self, meta_list):
        for meta in meta_list:
            if meta == '用户名':
                print self.text_proces.color(meta + ':' + self.__user.name, 'blue', 'l')
            else:
                meta_ob = self.__user.meta_dict.get(meta)
                if meta != "用户密码":
                    print self.text_proces.color(meta_ob.name + ':' + meta_ob.value, 'blue', 'l')


    def regist_account(self, meta_list, meta_dict):
        for meta in meta_list:
            types = meta_dict.get(meta)
            while(True):
                result = self.__input_regist_info(meta) #调用内部输入方法，返回规则检测信息
                if result == True:
                    if meta == '用户名':
                        self.__create_user(self.__tmp_var)
                        break
                    else:
                        self.__user.add_meta(meta, self.__tmp_var, types)
                        break
                else:
                    print self.text_proces.color(result, 'red', 'l')
        self.__display_regist_info(meta_list) #显示注册信息
        print '输入验证码'
        if True:
            if self.__user.get_id() == False:
                result = True if self.__insert_regist_info() else False #注册信息插入数据库
            else:
                print self.text_proces.color('用户名已存在！', 'red', 'l')
                result = False
        return result


    def login_account(self, meta_list, meta_dict):
        for meta in meta_list:
            types = meta_dict.get(meta)
            self.__input_login_info(meta)
            if meta == '用户名':
                self.__create_user(self.__tmp_var)
            else:
                self.__user.add_meta(meta, self.__tmp_var, types)
        print '输入验证码'
        if True:
            for meta in meta_list:
                if meta == '用户名':
                    if self.load_user(self.__user.name) == False: #从数据库读取用户
                        print self.text_proces.color('用户名不存在！', 'red', 'l')
                        return False
                else:
                    meta_ob = self.__user.meta_dict[meta] #获取属性对象
                    self.user.load_meta(meta_ob.name) #从数据库读取用户属性
                    if self.user.meta.cmp_value(meta_ob):
                        print '%s正确！' % meta
                        # result = self.mysql.check_ulocked_status(self.__user.ID, meta_ob.ID)
                        # if result == True:
                            # print self.text_proces.color('登入成功！', 'green', 'l')
                            # result = True
                        # else:
                            # print self.text_proces.color(result , 'red', 'l')
                            # result = False
                    else:
                        print '%s错误！' % meta
                        result = self.mysql.usermeta_worng_proces(self.user, 3, 10)
                        if type(result) == str:
                            print self.text_proces.color(result , 'red', 'l')

        # return result


    def construct_user(self):
        pass


    def display_account_info(self, name):
        self.__get_user_ob(name)
        tmp = '用户名:     ' + self.__user.name
        print self.text_proces.color(tmp, 'blue', 'l')
        for meta in self.__user.meta_list:
            if meta.name != "用户密码":
                tmp = meta.name + ':     ' + meta.value
                print self.text_proces.color(tmp, 'blue', 'l')


'''定义函数'''


'''程序开始'''
# ob = MyBank()
# ob.load_user('mp4102')
# print ob.user.name
# ob.user.load_meta('用户密码')
# print ob.user.meta.name, ob.user.meta.value, ob.user.meta.user_id
# ob.__display_regist_info
# now_time = datetime.datetime.now()
# name = 'zneglei'
# genre = 'vip'
# print genre,type(genre)
# ob = TextProces()
# print ob.get_types(name)
# a = str(type(name))
# d = a.strip("<>").strip("type ").strip("'")
# mysql = MySQL()
# res = mysql.load_user(2)
# for ss in res:
    # ss = ss.encode('utf-8') if type(ss) == unicode else ss
    # print ss, type(ss)
# print mysql.create_user_table()
# print mysql.create_usermeta_table()
# print mysql.create_userwrong_table()
# print mysql.load_userwrong(2,1)
# print mysql.load_ulocked_wrong_count(8,11)
# mysql.create_user_locked_table()
# print mysql.load_umeta_id(5, '用户密码')
# print mysql.load_umeta_value(5, '用户密码')
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
