#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''类的集成模块'''

# if __name__ == '__main__':
# import __init__

'''导入模块'''

from MyBanks import MyBank

'''定义常量'''
REGIST_META_ORDER = ["用户名", "用户密码", "电子邮箱", "手机"]
LOGIN_META_ORDER = ['用户名', '用户密码']
META_GENRE_LIST = ["账户安全", "个人信息",  "收货信息", "资产信息"]
META_DICT = {
    "用户名": 'str',
    "用户密码": 'str',
    "电子邮箱": 'str',
    "手机": 'str'
}

'''定义类'''

'''定义函数'''

'''程序开始'''

ob = MyBank()
# print ob.regist_account(REGIST_META_ORDER, META_DICT)
print ob.login_account(LOGIN_META_ORDER, META_DICT)
# ob.regist_account(REGIST_META_ORDER, META_DICT)
# ob.load_user(2)
# ob.display_regist_info(REGIST_META_ORDER)
