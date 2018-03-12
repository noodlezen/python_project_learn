#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    print 'my_API_mysql.py以主程运行！ '
    import __init__

import re
import MySQLdb
from my_bin import my_proces_text

DB_HOST = 'localhost'
DB_USERNAME = 'noodlezen'
DB_PASSWORD = 'asd123'
DB_NAME = 'Web_Shop_User_DB'

# __SQL_DICT = {
# 'SELECT': 0,
# 'CREATE': 2,
# 'DELETE': 2,
# 'UPDATE': 0,
# 'INSERT INTO': 0,
# 'WHERE': 0,
# 'AND': 0,
# 'OR': 0
# }


def create_database(p_db_name):
    db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD)
    cursor = db.cursor()
    sql = "CREATE DATABASE %s" % p_db_name
    try:
        cursor.execute(sql)
        result = p_db_name
        temp = "数据库：%s 创建成功！" % p_db_name
        print my_proces_text.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据库：%s 创建失败！" % p_db_name
        print my_proces_text.color(temp, 'red', 'l')
    db.close()
    return result


def delete_database(p_db_name):
    db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD)
    cursor = db.cursor()
    sql = "DROP DATABASE %s" % p_db_name
    try:
        cursor.execute(sql)
        result = p_db_name
        temp = "数据库：%s 删除成功！" % p_db_name
        print my_proces_text.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据库：%s 删除失败！" % p_db_name
        print my_proces_text.color(temp, 'red', 'l')
    db.close()
    return result


def create_table(p_db_name, p_table):
    db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, p_db_name)
    cursor = db.cursor()
    # sql = "CREATE TABLE %s (FIRST_NAME CHAR(20) NOT NULL,LAST_NAME CHAR(20),AGE INT,INCOME FLOAT)" % p_table
    sql = "CREATE TABLE %s (USERNAME CHAR(20),PASSWORD CHAR(20))" % p_table
    try:
        cursor.execute(sql)
        result = p_table
        temp = "数据表：%s 创建成功！" % p_table
        print my_proces_text.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据表：%s 创建失败！" % p_table
        print my_proces_text.color(temp, 'red', 'l')
    db.close()
    return result


def delete_table(p_db_name, p_table):
    db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, p_db_name)
    cursor = db.cursor()
    sql = "DROP TABLE %s" % p_table
    try:
        cursor.execute(sql)
        result = p_table
        temp = "数据表：%s 删除成功！" % p_table
        print my_proces_text.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据表：%s 删除失败！" % p_table
        print my_proces_text.color(temp, 'red', 'l')
    db.close()
    return result


def clear_table(p_db_name, p_table):
    db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, p_db_name)
    cursor = db.cursor()
    sql = "DELETE FROM %s" % p_table
    try:
        cursor.execute(sql)
        db.commit()
        result = p_table
        temp = "数据表：%s 记录清空成功！" % p_table
        print my_proces_text.color(temp, 'green', 'l')
    except:
        db.rollback()
        result = False
        temp = "数据表：%s 记录清空失败！" % p_table
        print my_proces_text.color(temp, 'red', 'l')
    db.close()
    return result


def update_table(p_db_name, p_table, p_key, p_value):
    db = MySQLdb.connect(DB_HOST, DB_USERNAME,
                         DB_PASSWORD, p_db_name, charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE %s SET PASSWORD = 'max' WHERE %s = '%s'" % (
        p_table, p_key, p_value)
    # sql = "INSERT INTO %s(USERNAME,PASSWORD) VALUES ('%s','%s')" % (p_table, p_key, p_value)
    try:
        cursor.execute(sql)
        db.commit()
        result = p_table
        temp = "数据表：%s 更新成功！" % p_table
        print my_proces_text.color(temp, 'green', 'l')
    except:
        db.rollback()
        result = False
        temp = "数据表：%s 更新失败！" % p_table
        print my_proces_text.color(temp, 'red', 'l')
    db.close()
    return result


def insert_table(p_db_name, p_table, p_value1, p_value2):
    db = MySQLdb.connect(DB_HOST, DB_USERNAME,
                         DB_PASSWORD, p_db_name, charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO %s VALUES ('%s','%s')" % (p_table, p_value1, p_value2)
    # sql = "INSERT INTO %s(USERNAME,PASSWORD) VALUES ('%s','%s')" % (p_table, p_key, p_value)
    try:
        cursor.execute(sql)
        db.commit()
        result = p_table
        temp = "数据表：%s 插入记录成功！" % p_table
        print my_proces_text.color(temp, 'green', 'l')
    except:
        db.rollback()
        result = False
        temp = "数据表：%s 插入记录失败！" % p_table
        print my_proces_text.color(temp, 'red', 'l')
    db.close()
    return result


def select(p_db_name, p_table, p_key_1, p_value, p_key_2):  # 取p_key_1 = p_value 的 p_key_2 的值
    db = MySQLdb.connect(DB_HOST, DB_USERNAME,
                         DB_PASSWORD, p_db_name, charset='utf8')
    cursor = db.cursor()
    # sql = "SELECT %s FROM %s" % (p_key, p_table)
    sql = "SELECT %s FROM %s WHERE %s = '%s'" % (
        p_key_2, p_table, p_key_1, p_value)  # 取USERNAME = test_2 的 PASSWORD
    try:
        cursor.execute(sql)
        args = cursor.fetchall()
        for i in args:
            print i[0]

        result = p_table
        temp = "数据表：%s 读取成功！" % p_table
        print my_proces_text.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据表：%s 读取失败！" % p_table
        print my_proces_text.color(temp, 'red', 'l')
    db.close()
    return result


def SQL(p_db_name, p_str):
    db = MySQLdb.connect(DB_HOST, DB_USERNAME,
                         DB_PASSWORD, p_db_name, charset='utf8')
    cursor = db.cursor()
    sql_cmd = p_str.split(' ')[0]
    try:
        cursor.execute(p_str)
        db.commit()
        if sql_cmd == 'SELECT':
            result = cursor.fetchall()
            # result = result.decode('utf-8').encode('gbk')
        else:
            result = True
        temp = "%s:成功！" % sql_cmd
        print my_proces_text.color(temp, 'green', 'l')

    except:
        db.rollback()
        result = False
        temp = "%s:失败！" % sql_cmd
        print my_proces_text.color(temp, 'red', 'l')
    db.close()
    return result


def user_info_insert_mysql(p_db_name,p_ob):#把用户对象插入mysql数据库
    # print p_ob.apellation, p_ob.genre, p_ob.created

    sql_cmd = "INSERT INTO User(USER_APELLATION, USER_GENRE, USER_CREATED) VALUES ('%s','%s','%s')" % (
        p_ob.apellation, p_ob.genre, p_ob.created)
    result = SQL(p_db_name, sql_cmd)#插入用户对象名，用户对象类型，创建时间，到数据库。

    for items_feature in p_ob.feature_array:#循环遍历用户对象的 属性信息。
        # print p_ob.apellation, items_feature.apellation, items_feature.genre, items_feature.created

        sql_cmd = "INSERT INTO User_Feature(USER_APELLATION, FEATURE_APELLATION, FEATURE_GENRE, FEATURE_MODIFIED_COUNT, FEATURE_CREATED) VALUES ('%s','%s','%s',%d,'%s')" % (
            p_ob.apellation, items_feature.apellation, items_feature.genre, items_feature.modified_count, items_feature.created)
        result = SQL(p_db_name, sql_cmd)#插入用户对象名，特征名，特征类型，修改次数，创建时间，到数据库。

        for items_record in items_feature.record_array:#循环遍历用户特征对象的 记录信息。
            # print items_record.apellation, items_record.genre, items_record.num, items_record.created

            # if items_feature.apellation == "密码":#给密码加密5dm
                # items_record.num = my_proces_text.encrypt_str(items_record.num)

            sql_cmd = "INSERT INTO User_Feature_Record(USER_APELLATION, FEATURE_APELLATION, RECORD_APELLATION, RECORD_GENRE, RECORD_NUM, RECORD_CREATED) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                p_ob.apellation, items_feature.apellation, items_record.apellation, items_record.genre, items_record.num, items_record.created)
            result = SQL(p_db_name, sql_cmd)#插入用户对象名，特征名，记录名，记录类型，记录值，创建时间，到数据库。


def user_load_record_mysql(p_db_name, p_username, p_feature):
    #读出特征修改数
    sql_cmd = "SELECT FEATURE_MODIFIED_COUNT FROM User_Feature WHERE USER_APELLATION = '%s' AND FEATURE_APELLATION = '%s'" % (p_username, p_feature) # 查询数据库
    result = SQL(p_db_name, sql_cmd)  # 以元组形式返回匹配到的结果。
    if len(result) != 0:
        if result[0][0] != 0:
            p_record = '当前记载'
        else:
            p_record = '初始记载'
        #读出对应名称的记载值
        sql_cmd = "SELECT RECORD_NUM FROM User_Feature_Record WHERE USER_APELLATION = '%s' AND FEATURE_APELLATION = '%s' AND RECORD_APELLATION = '%s'" % (p_username, p_feature, p_record) # 查询数据库
        result = SQL(p_db_name, sql_cmd)  # 以元组形式返回匹配到的结果。
        if len(result) != 0:
            return result[0][0]
        else:
            return False
    else:
        return False


def user_password_cmp_mysql(p_db_name, p_ob):
    username = p_ob.apellation
    password = p_ob.feature_wordbook['密码'].record.num
    db_password = user_load_record_mysql(p_db_name, username, '密码')
    if db_password != False:
        if password == db_password:
            return True
        else:
            return False
    else:
        return False


def user_password_wrong_proces(p_db_name, p_ob, p_toplimit, p_duration):
    sql_cmd = "SELECT WRONG_COUNT FROM User_Locked WHERE USER_APELLATION = '%s'" % p_ob.apellation# 查询数据库
    result = SQL(p_db_name, sql_cmd)  # 以元组形式返回匹配到的结果。
    if len(result) == 0: #账户添加到名单,并记录错误次数，返回原因。
        wrong_count = 1
        reason = '密码错误！您还有%d次机会尝试登入！' % (p_toplimit - 1)
        result = p_ob.locked(p_db_name, reason, p_duration, wrong_count)
        if result == True: #锁定成功，返回理由
            return reason
        else:
            return False

    else: #累积错误次数，检查是否超时，更新原因
        wrong_count = result[0][0] + 1
        result = p_ob.check_lock_state(p_db_name)
        if result == True: #锁定时间到，解除锁定。
            result = p_ob.unlock(p_db_name)
            if result == True:
                result = '密码错误！您还有%d次机会尝试登入！' % p_toplimit
                return result
            else:
                return False
        else: #更新原因

            if wrong_count >= p_toplimit: #错误次数超出限额
                reason = '账户已锁定！登入密码错误次数超过限制,请在%d分钟后再次尝试登入！' % int(result / 60)
            else:
                reason = '密码错误！您还有%d次机会尝试登入！' % (p_toplimit - wrong_count)

            sql_cmd = "UPDATE User_Locked SET WRONG_COUNT = %d WHERE USER_APELLATION = '%s'" % (
            wrong_count, p_ob.apellation) #更新错误次数
            result = SQL(p_db_name, sql_cmd)
            sql_cmd = "UPDATE User_Locked SET REASON = '%s' WHERE USER_APELLATION = '%s'" % (
            reason, p_ob.apellation) #更新理由
            result = (result & SQL(p_db_name, sql_cmd))
            if result == True: #更新成功
                return reason
            else:
                return False


def user_locked_check(p_db_name, p_ob, p_toplimit):
    sql_cmd = "SELECT WRONG_COUNT FROM User_Locked WHERE USER_APELLATION = '%s'" % p_ob.apellation# 查询数据库
    result = SQL(p_db_name, sql_cmd)  # 以元组形式返回匹配到的结果。
    if len(result) != 0:
        wrong_count = result[0][0]
        if wrong_count >= p_toplimit: #错误次数超过限制，检查锁定时间
            result = p_ob.check_lock_state(p_db_name)
            if result == True: #锁定时间到，解除锁定
                result = p_ob.unlock(p_db_name)
                return result
            else: #账户已被锁定，更新理由
                reason = '账户已锁定！登入密码错误次数超过限制,请在%d分钟后再次尝试登入！' % int(result / 60)
                sql_cmd = "UPDATE User_Locked SET REASON = '%s' WHERE USER_APELLATION = '%s'" % (
                reason, p_ob.apellation) #更新理由
                result = SQL(p_db_name, sql_cmd)
                if result == True:
                    return reason
                else:
                    return False
        else: #错误次数不足，解除锁定,可正常登入
            result = p_ob.unlock(p_db_name)
            return result
    else: #账户没有被锁定,可正常登入
        return True



'''
ob_username = 'mp4102'

# sql_cmd = "SELECT RECORD_NUM FROM User_Feature_Record WHERE USER_APELLATION = '%s' AND FEATURE_APELLATION = '密码'" % (ob_username) # 查询数据库
# result = SQL('Web_Shop_User_DB', sql_cmd)  # 以元组形式返回匹配到的结果。
# print result[0][0]

sql_cmd = "SELECT * FROM User_Feature_Record WHERE FEATURE_APELLATION = '密码' ORDER BY USER_APELLATION" # 查询数据库
result = SQL('Web_Shop_User_DB', sql_cmd)  # 以元组形式返回匹配到的结果。

if len(result) != 0:
    print result
    for items in result:
        print items
        print items[0]
'''
