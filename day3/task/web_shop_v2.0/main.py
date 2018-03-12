#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import time
import md5

from my_bin import my_Class_User
from my_bin import my_API_mysql
from my_bin import my_proces_text
from my_bin import my_interactive_fill_info
from my_bin import my_interactive_validate

'''定义常量'''
my_API_mysql.DB_HOST = 'localhost'
my_API_mysql.DB_USERNAME = 'noodlezen'
my_API_mysql.DB_PASSWORD = 'asd123'
my_API_mysql.DB_NAME = 'Web_Shop_User_DB'

'''定义函数'''


def welcome_page():
    print my_proces_text.color('''
    欢迎光临33网上商城！
    ''', 'red', 'l')


def regist_page():
    print my_proces_text.color('''
    注册账户！
    ''', 'green', 'l')


def login_page():
    print my_proces_text.color('''
    账户登入！
    ''', 'green', 'l')


def account_login():
    result = None
    al_flag_1 = 1
    password_error = 0
    while(al_flag_1 != 'q'):
        login_page() #显示登入页面
        al_flag_1 = raw_input("是否开始登入？\n(y/n):  ")
        if al_flag_1 == 'y':

            ob_user = my_interactive_fill_info.fill_login_info(my_API_mysql.DB_NAME)
            result = my_interactive_validate.text_validate() #调用my_interactive_validate模块的文本验证方法

            if result == True: #对比密码是否正确
                result = my_API_mysql.user_password_cmp_mysql(my_API_mysql.DB_NAME, ob_user)
                if result == True: #密码正确，检测锁定状态
                    result = my_API_mysql.user_locked_check(my_API_mysql.DB_NAME, ob_user, 3)
                    if result == True: #没有被锁定，登入成功，退出循环并返回用户对象
                        print my_proces_text.color('%s登入成功！' % ob_user.apellation,'green','l')
                        result = ob_user
                        al_flag_1 = 'q'
                    else: #账户以为锁定，返回带有剩余时间的错误信息
                        print my_proces_text.color(result, 'red', 'l')
                        result = False

                else: #密码错误，记录错误次数，返回错误信息
                    result = my_API_mysql.user_password_wrong_proces(my_API_mysql.DB_NAME, ob_user, 3, 10) #错误上限为3次 ，锁定时间为10分钟
                    if type(result) == str:
                        print my_proces_text.color(result, 'red', 'l')
                    else:
                        result = False

        elif al_flag_1 == 'n':
            al_flag_1 = 'q'
    else:
        print '退出登入页面！'
        return result


def account_regist():
    result = None
    ar_flag_1 = 1
    while(ar_flag_1 != 'q'):
        regist_page() #显示注册页面
        ar_flag_1 = raw_input("是否开始注册？\n(y/n):  ")
        if ar_flag_1 == 'y':

            ob_user = my_interactive_fill_info.fill_regist_info(my_API_mysql.DB_NAME) #调用my_interactive_fill_info模块的注册账户方法，内置规则检测，返回构建好基础数据的用户对象。
            my_interactive_fill_info.display_regist_info(ob_user) #调用my_interactive_fill_info模块的显示注册信息方法。

            result = my_interactive_validate.text_validate() #调用my_interactive_validate模块的文本验证方法

            # ob_user.feature.update_record('str','12306')
            # ob_user.feature.update_record('str','88888')

            if result == True :
                my_API_mysql.user_info_insert_mysql(my_API_mysql.DB_NAME,ob_user)#调用my_API_mysql模块的数据库插入方法，上传信息到数据库。
                print my_proces_text.color("注册成功！密码以加密！写入MySQL数据库！",'green','l')
                result = ob_user #注册成功返回用户对象
                ar_flag_1 = 'q'

        elif ar_flag_1 == 'n':
            ar_flag_1 = 'q'
    else:
        print '退出注册页面！'
        return result


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
main()
# ob = account_regist()
# ob = account_login()
