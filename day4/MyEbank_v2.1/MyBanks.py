#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''Bnak类模块'''
# if __name__ == '__main__':
# print 'error'

'''导入模块'''
import datetime
from MyAccount import *
from MyTools import *
from MyDateBase import *

'''定义常量'''

'''定义类'''


class Basic(object):
    def __init__(self):
        self.text_rule = TextRule()
        self.text_proces = TextProces()
        self.mysql = MySQL()

    def load_user(self, user_name):
        user_dict = self.mysql.xload_user(user_name)
        if user_dict != False:
            user_id = user_dict['user_id']
            name = user_dict['user_name']
            genre = user_dict['user_genre']
            status = user_dict['user_status']
            created = user_dict['user_created']
            self.user = User(name, genre, user_id, status, created, user_dict)
            return True
        else:
            return False

    def __input_info(self, keys):
        self.__input_var = raw_input("请输入%s:  " % keys)

    def print_info(self, text, color='0', *args):
        print self.text_proces.color(text, color, *args)

    def display_user_info(self, user, meta_list):
        for meta_name in meta_list:
            if meta_name == '用户名':
                print self.text_proces.color(
                    meta_name + ':' + user.name, 'blue', 'l')
            else:
                meta = user.meta_dict.get(meta_name)
                if meta_name != "用户密码":
                    print self.text_proces.color(
                        meta_name + ':' + meta.value, 'blue', 'l')


class Regist(Basic, object):
    def __init__(self):
        Basic.__init__(self)

    def __add_ghost(self, ghost_name, genre=None):
        self.__ghost = User(ghost_name, genre)  # 创建零时用户对象

    def __input_info(self, meta_name):
        self.__input_var = raw_input("请输入%s:  " % meta_name)
        if meta_name == '用户密码':
            re_input_var = raw_input("请再次输入%s:  " % meta_name)
            if self.__input_var == re_input_var:
                result = self.text_rule.check_meta_value(
                    meta_name, self.__input_var)  # 调用文本规则检测
                if result == True:
                    self.__input_var = self.text_proces.encrypt(
                        self.__input_var)  # 给用户密码加密
                    return True
                else:
                    return result  # 返回错误信息
            else:
                return '用户密码不一致，请重新输入！'
        # 不是密码直接调用文本规则检测
        return self.text_rule.check_meta_value(meta_name, self.__input_var)

    def __insert_datebase(self, user):
        if user.insert_datebase():  # 插入数据库
            if user.get_id() != False:  # 获得数据库ID
                for meta in user.meta_list:
                    if not meta.insert_datebase(user.ID):  # 插入数据库
                        return False
                return True
            else:
                return False
        else:
            return False

    def regist_account(self, meta_list, meta_dict):
        for meta_name in meta_list:
            meta_types = meta_dict.get(meta_name)
            while(True):
                result = self.__input_info(meta_name)  # 调用内部输入方法，返回规则检测信息
                if result == True:
                    if meta_name == '用户名':
                        self.__add_ghost(self.__input_var)
                        break
                    else:
                        self.__ghost.add_meta(
                            meta_name, self.__input_var, meta_types)
                        break
                else:
                    print self.text_proces.color(result, 'red', 'l')
        self.display_user_info(self.__ghost, meta_list)  # 显示注册信息
        print '输入验证码'
        if True:
            if self.__ghost.get_id() == False:
                result = True if self.__insert_datebase(
                    self.__ghost) else False  # 注册信息插入数据库
            else:
                print self.text_proces.color('用户名已存在！', 'red', 'l')
                result = False
        return result


class Login(Basic, object):
    def __init__(self):
        Basic.__init__(self)

    def __add_ghost(self, ghost_name, genre=None):
        self.__ghost = User(ghost_name, genre)  # 创建零时用户对象

    def __input_info(self, meta_name):
        self.__input_var = raw_input("请输入%s:  " % meta_name)
        if meta_name == '用户密码':
            self.__input_var = self.text_proces.encrypt(
                self.__input_var)  # 给用户密码加密

    def __meta_worng_proces(self, user, toplimit, duration):
        if not user.meta.load_wrong():  # 从数据库读取错误对象
            name = '%s错误！您还有%d次机会尝试！' % (user.meta.name, toplimit - 1)
            user.meta.add_wrong(name, '登入错误', toplimit, duration)  # 添加属性错误信息
            user.meta.wrong.insert_datebase()  # 插入数据库
            return name
        else:
            remain_time = user.meta.wrong.check_duration()  # 判断是否过期
            if remain_time == False:
                user.meta.wrong.delete_wrong()  # 删除无效错误信息
                return '%s错误！您还有%d次机会尝试！' % (user.meta.name, user.meta.wrong.toplimit)
            else:
                user.meta.wrong.modify_count(user.meta.wrong.count + 1)  # 累积次数
                remain_count = user.meta.wrong.check_count()  # 检测剩余次数
                if remain_count == False:  # 错误次数超出限额
                    user.meta.wrong.modify_name('账户已锁定！%s错误次数超过限制,请在%d分钟后再次尝试登入！' % (
                        user.meta.name, int(remain_time / 60)))  # 修改错误信息
                    user.lock(user.meta.wrong.ID)  # 锁定用户对象
                    result = user.meta.wrong.name
                else:
                    result = '%s错误！您还有%d次机会尝试！' % (
                        user.meta.name, remain_count)
                user.meta.wrong.update_datebase()  # 更新属性错误修改信息到数据库
                user.update_datebase()  # 更新用户修改信息到数据库
                return result

    def login_account(self, meta_list, meta_dict):
        result = True
        for meta_name in meta_list:
            meta_types = meta_dict.get(meta_name)
            self.__input_info(meta_name)
            if meta_name == '用户名':
                self.__add_ghost(self.__input_var)
            else:
                self.__ghost.add_meta(meta_name, self.__input_var, meta_types)
        print '输入验证码'
        if True:
            for meta_name in meta_list:
                if meta_name == '用户名':
                    if self.load_user(self.__ghost.name) == False:  # 从数据库读取用户
                        self.print_info('用户名不存在！', 'red', 'l')
                        return False
                    else:
                        result = self.user.check_status()  # 检测用户状态，返回Ture或错误id
                        if result != True:
                            self.user.load_wrong(wrong_id=result)  # 根据id读取错误对象
                            remain_time = self.user.wrong.check_duration()  # 检测是否过期
                            if remain_time == False:
                                self.user.unlock()  # 用户解锁
                                self.user.update_datebase()  # 用户对象更新数据库
                            else:
                                self.print_info('账户已锁定！请在%d分钟后再次尝试登入！' % int(
                                    remain_time / 60), 'red', 'l')
                                return False
                else:
                    __meta = self.__ghost.meta_dict[meta_name]  # 获取零时用户属性对象
                    self.user.load_meta(__meta.name)  # 从数据库读取用户属性
                    if self.user.meta.cmp_value(__meta):  # 判断是否相等
                        if self.user.meta.load_wrong():  # 读取是否有无效属性错误记录
                            self.user.meta.wrong.delete_wrong()  # 删除无效错误记录
                            # delattr(self.user.meta, 'wrong')
                        self.print_info('登入成功！', 'green', 'l')
                        res = True
                    else:
                        result = self.__meta_worng_proces(
                            self.user, 3, 1)  # 调用密码错误处理
                        if result != False:
                            self.print_info(result, 'red', 'l')  # 输出错误信息
                        res = False
                    result = result and res
            return result
        else:
            self.print_info('验证码错误！请重新输入！', 'red', 'l')
            return False


class MyBank(Regist, Login, object):
    def __init__(self):
        Regist.__init__(self)
        Login.__init__(self)
