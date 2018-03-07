#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from my_bin import my_Class_User
from my_bin import my_proces_text

'''定义常量'''
BASIC_FEATURE_ORDER = ["用户名", "密码", "电子邮箱","手机"]
FEATURE_GENRE_ARRAY_L = ["个人信息", "账户安全", "收货信息", "资产信息"]
FEATURE_ARRAY_D = {"用户名": FEATURE_GENRE_ARRAY_L[0],
                   "密码": FEATURE_GENRE_ARRAY_L[1],
                   "电子邮箱": FEATURE_GENRE_ARRAY_L[0],
                   "手机": FEATURE_GENRE_ARRAY_L[2]}

'''定义变量'''

'''定义函数'''

def fill_regist_info():

    for items in BASIC_FEATURE_ORDER:
        if items == "用户名":

            tmp_var = raw_input("请输入%s:  " % items)
            ob_user = my_Class_User.User(tmp_var,"vip") #构建用户
            ob_user.create_feature(items,FEATURE_ARRAY_D.get(items)) #构建用户属性
            ob_user.feature.create_record('str', tmp_var) #构建用户属性记载

        elif items == "密码":

            while(True):
                tmp_var_1 = raw_input("请输入%s:  " % items)
                tmp_var_2 = raw_input("请再次输入%s:  " % items)
                if tmp_var_1 == tmp_var_2:
                    break
                else:
                    print my_proces_text.color("密码不一致，请重新输入！", 'red', 'l')

            ob_user.create_feature(items,FEATURE_ARRAY_D.get(items)) #构建用户属性
            ob_user.feature.create_record('str', tmp_var_1) #构建用户属性记载

        else:
            tmp_var = raw_input("请输入%s:  " % items)
            ob_user.create_feature(items, FEATURE_ARRAY_D.get(items)) #构建用户属性
            ob_user.feature.create_record('str', tmp_var) #构建用户属性记载

    return ob_user #返回用户对象

def display_regist_info(p_ob):
    for items_feature in p_ob.feature_array:
        for items_record in items_feature.record_array:
            if items_feature.apellation != "密码":
                tmp_strng = items_feature.apellation + ':     ' + items_record.num
                print my_proces_text.color(tmp_strng,'blue','l')

    # feature_genre_array_d = {}
    # for items in p_ob.feature_array: #把属性类型放入字典，key为类型名，value存放重复次数。
        # if feature_genre_array_d.has_key(items.genre):
            # feature_genre_array_d[items.genre] += 1
        # else:
            # feature_genre_array_d[items.genre] = 1

'''程序开始'''

# ob_user = fill_regist_info()

# display_regist_info(ob_user)

# for i in ob_user.feature_array:
        # print i.record_count
        # for j in i.record_array:
            # print j.apellation, j.genre, j.num
        # print i.apellation, i.genre


