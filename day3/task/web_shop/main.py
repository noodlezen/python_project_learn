#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import time
import md5
from bin import format_str
from bin import build_user
from data import mysql
import fill_info

'''定义常量'''
mysql.MYSQL_HOST = 'localhost'
mysql.MYSQL_USERNAME = 'noodlezen'
mysql.MYSQL_PASSWORD = 'asd123'
mysql.MYSQL_DB_NAME = 'Web_Shop_User_DB'

'''定义函数'''


def welcome_page():
    print format_str.color('''
    欢迎光临33网上商城！
    ''', 'red', 'l')


def regist_page():
    print format_str.color('''
    注册账户！
    ''', 'green', 'l')


def account_login():
    pass


def account_regist():
    ar_flag_1 = 1
    while(ar_flag_1 != 'q'):
        regist_page() #显示注册页面
        ar_flag_1 = raw_input("是否开始注册？\n(y/n):  ")
        if ar_flag_1 == 'y':
            ob_user = fill_info.fill_regist_info() #调用fill_info模块的注册账户方法，返回构建好基础数据的用户对象。
            fill_info.display_regist_info(ob_user) #调用fill_info模块的显示注册信息方法。

            ar_flag_2 = raw_input("是否提交？\n(y/n):  ")
            if ar_flag_2 == 'y':
                result = mysql.regist_info_rc(ob_user) #调用mysql模块的规则检查方法，返回错误信息字符串，无措返回True。
                if result == True:
                    print '注册成功，密码加密，写入MySQL数据库'
                    mysql.user_info_update_mysql(ob_user)
                    ar_flag_1 = 'q'
                else:
                    print result

        elif ar_flag_1 == 'n':
            ar_flag_1 = 'q'
    else:
        print '退出注册页面！'


def start_shopping():
    print 'shopping'


def user_center():
    print 'user center'


def main():
    m_flag_1 = 1
    while(m_flag_1 != 'q'):
        welcome_page()  # 显示欢迎界面。
        m_flag_1 = raw_input("请输入:  ")
        if m_flag_1 == '1':
            account_login()  # 调用账户登入函数
        elif m_flag_1 == '2':
            account_regist()  # 调用账户注册函数
        elif m_flag_1 == '3':
            start_shopping()  # 调用开始购物函数
        elif m_flag_1 == '4':
            user_center()  # 调用用户中心
    else:
        print "谢谢惠顾！"


'''程序开始'''
# main()
account_regist()
