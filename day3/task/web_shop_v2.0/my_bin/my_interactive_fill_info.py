#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    import __init__

from my_bin import my_Class_User
from my_bin import my_proces_text
from my_bin import my_API_mysql


'''定义常量'''

REGIST_FEATURE_ORDER = ["用户名", "密码", "电子邮箱","手机"]
LOGIN_FEATURE_ORDER = ['用户名', '密码']
FEATURE_GENRE_ARRAY = ["个人信息", "账户安全", "收货信息", "资产信息"]
FEATURE_WORDBOOK = {"用户名": (FEATURE_GENRE_ARRAY[0], 'str'),
    "密码": (FEATURE_GENRE_ARRAY[1], 'str'),
    "电子邮箱": (FEATURE_GENRE_ARRAY[0], 'str'),
    "手机": (FEATURE_GENRE_ARRAY[2], 'str')
                   }

'''定义变量'''

'''定义函数'''

def display_regist_info(p_ob):
    tmp_strng ='用户名:     ' + p_ob.apellation
    print my_proces_text.color(tmp_strng,'blue','l')
    for items_feature in p_ob.feature_array:
        for items_record in items_feature.record_array:
            if items_feature.apellation != "密码":
                tmp_strng = items_feature.apellation + ':     ' + items_record.num
                print my_proces_text.color(tmp_strng,'blue','l')


def fill_regist_info(p_db_name):

    for items in REGIST_FEATURE_ORDER:
        tmp_array = FEATURE_WORDBOOK.get(items)
        while(True):
            tmp_var = raw_input("请输入%s:  " % items)
            if items == '用户名':
                result = my_Class_User.create_user(tmp_var, db_apellation = p_db_name) #检测规则和重名，并创建用户对象
                if type(result) != str:
                    ob_user = result
                    break
                else:
                    print my_proces_text.color(result,'red','l')

            elif items == '密码':
                tmp_var_2 = raw_input("请再次输入%s:  " % items)
                if tmp_var == tmp_var_2:
                    ob_user.create_feature(items, tmp_array[0])
                    result = ob_user.feature.create_record(tmp_array[1], tmp_var)
                    if result != True:
                        print my_proces_text.color(result,'red','l')
                    else:
                        break
                else:
                    print my_proces_text.color('密码不一致，请重新输入！','red','l')

            else:
                ob_user.create_feature(items, tmp_array[0])
                result = ob_user.feature.create_record(tmp_array[1], tmp_var)
                if result != True:
                    print my_proces_text.color(result,'red','l')
                else:
                    break
    return ob_user


def fill_login_info(p_db_name):
    for items in LOGIN_FEATURE_ORDER:
        tmp_array = FEATURE_WORDBOOK.get(items)
        while(True):
            tmp_var = raw_input("请输入%s:  " % items)
            if items == '用户名':

                result = my_Class_User.login_user(tmp_var, db_apellation = p_db_name) #检测规则和重名，并创建用户对象
                if type(result) != str:
                    ob_user = result
                    break
                else:
                    print my_proces_text.color(result,'red','l')

            else:
                ob_user.create_feature(items, tmp_array[0])
                result = ob_user.feature.create_record(tmp_array[1], tmp_var)
                if result != True:
                    print my_proces_text.color(result,'red','l')
                else:
                    break
    return ob_user


'''程序开始'''

# ob_user = fill_regist_info()

# display_regist_info(ob_user)

# for i in ob_user.feature_array:
        # print i.record_count
        # for j in i.record_array:
            # print j.apellation, j.genre, j.num
        # print i.apellation, i.genre


