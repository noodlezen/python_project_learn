#!/usr/bin/env python
#_*_ coding:utf-8 _*_

MYSQL_HOST = 'localhost'
MYSQL_USERNAME = 'noodlezen'
MYSQL_PASSWORD = 'asd123'
# MYSQL_DB_NAME = 'Web_Shop_User_DB'

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

if __name__ == '__main__':
    print 'mysql.py以主程运行！ '
    import __init__

import re
import MySQLdb
from bin import format_str


def create_database(p_db_name):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD)
    cursor = db.cursor()
    sql = "CREATE DATABASE %s" % p_db_name
    try:
        cursor.execute(sql)
        result = p_db_name
        temp = "数据库：%s 创建成功！" % p_db_name
        print format_str.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据库：%s 创建失败！" % p_db_name
        print format_str.color(temp, 'red', 'l')
    db.close()
    return result


def delete_database(p_db_name):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD)
    cursor = db.cursor()
    sql = "DROP DATABASE %s" % p_db_name
    try:
        cursor.execute(sql)
        result = p_db_name
        temp = "数据库：%s 删除成功！" % p_db_name
        print format_str.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据库：%s 删除失败！" % p_db_name
        print format_str.color(temp, 'red', 'l')
    db.close()
    return result


def create_table(p_db_name, p_table):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, p_db_name)
    cursor = db.cursor()
    # sql = "CREATE TABLE %s (FIRST_NAME CHAR(20) NOT NULL,LAST_NAME CHAR(20),AGE INT,INCOME FLOAT)" % p_table
    sql = "CREATE TABLE %s (USERNAME CHAR(20),PASSWORD CHAR(20))" % p_table
    try:
        cursor.execute(sql)
        result = p_table
        temp = "数据表：%s 创建成功！" % p_table
        print format_str.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据表：%s 创建失败！" % p_table
        print format_str.color(temp, 'red', 'l')
    db.close()
    return result


def delete_table(p_db_name, p_table):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, p_db_name)
    cursor = db.cursor()
    sql = "DROP TABLE %s" % p_table
    try:
        cursor.execute(sql)
        result = p_table
        temp = "数据表：%s 删除成功！" % p_table
        print format_str.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据表：%s 删除失败！" % p_table
        print format_str.color(temp, 'red', 'l')
    db.close()
    return result


def clear_table(p_db_name, p_table):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, p_db_name)
    cursor = db.cursor()
    sql = "DELETE FROM %s" % p_table
    try:
        cursor.execute(sql)
        db.commit()
        result = p_table
        temp = "数据表：%s 记录清空成功！" % p_table
        print format_str.color(temp, 'green', 'l')
    except:
        db.rollback()
        result = False
        temp = "数据表：%s 记录清空失败！" % p_table
        print format_str.color(temp, 'red', 'l')
    db.close()
    return result


def update_table(p_db_name, p_table, p_key, p_value):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME,
                         MYSQL_PASSWORD, p_db_name, charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE %s SET PASSWORD = 'max' WHERE %s = '%s'" % (
        p_table, p_key, p_value)
    # sql = "INSERT INTO %s(USERNAME,PASSWORD) VALUES ('%s','%s')" % (p_table, p_key, p_value)
    try:
        cursor.execute(sql)
        db.commit()
        result = p_table
        temp = "数据表：%s 更新成功！" % p_table
        print format_str.color(temp, 'green', 'l')
    except:
        db.rollback()
        result = False
        temp = "数据表：%s 更新失败！" % p_table
        print format_str.color(temp, 'red', 'l')
    db.close()
    return result


def insert_table(p_db_name, p_table, p_value1, p_value2):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME,
                         MYSQL_PASSWORD, p_db_name, charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO %s VALUES ('%s','%s')" % (p_table, p_value1, p_value2)
    # sql = "INSERT INTO %s(USERNAME,PASSWORD) VALUES ('%s','%s')" % (p_table, p_key, p_value)
    try:
        cursor.execute(sql)
        db.commit()
        result = p_table
        temp = "数据表：%s 插入记录成功！" % p_table
        print format_str.color(temp, 'green', 'l')
    except:
        db.rollback()
        result = False
        temp = "数据表：%s 插入记录失败！" % p_table
        print format_str.color(temp, 'red', 'l')
    db.close()
    return result


def select(p_db_name, p_table, p_key_1, p_value, p_key_2):  # 取p_key_1 = p_value 的 p_key_2 的值
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME,
                         MYSQL_PASSWORD, p_db_name, charset='utf8')
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
        print format_str.color(temp, 'green', 'l')
    except:
        result = False
        temp = "数据表：%s 读取失败！" % p_table
        print format_str.color(temp, 'red', 'l')
    db.close()
    return result


def SQL(p_db, p_str):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME,
                         MYSQL_PASSWORD, p_db, charset='utf8')
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
        print format_str.color(temp, 'green', 'l')

    except:
        db.rollback()
        result = False
        temp = "%s:失败！" % sql_cmd
        print format_str.color(temp, 'red', 'l')
    db.close()
    return result

def regist_info_rc(p_ob):
    for items_feature in p_ob.feature_array:
        for items_record in items_feature.record_array:

            if items_feature.apellation == "用户名":
                rule_error = format_str.check_username_rule(items_record.num)#调用format_str模块的用户名规则检查方法
                if rule_error == True:
                    sql_cmd = "SELECT USER_APELLATION FROM User WHERE USER_APELLATION = '%s'" % items_record.num  # 查询数据库
                    result = SQL('Web_Shop_User_DB',sql_cmd)  # 以元组形式返回匹配到的结果。
                    if len(result) != 0:
                        rule_error = format_str.color("用户名已存在！", 'red', 'l')
                        return rule_error
                else:
                    rule_error = format_str.color(rule_error,'red','l')
                    return rule_error

            elif items_feature.apellation == "密码":
                rule_error = format_str.check_password_rule(items_record.num,2)#调用format_str模块的密码规则检查方法
                if rule_error != True:
                    rule_error = format_str.color(rule_error,'red','l')
                    return rule_error

            elif items_feature.apellation == "电子邮箱":
                rule_error = format_str.check_email_rule(items_record.num)#调用format_str模块的电子邮箱规则检查方法
                if rule_error != True:
                    rule_error = format_str.color(rule_error,'red','l')
                    return rule_error
    rule_error = True
    return rule_error

def user_info_update_mysql(p_ob):
    print p_ob.apellation, p_ob.genre, p_ob.created
    for items_feature in p_ob.feature_array:
        print  items_feature.apellation, items_feature.genre, items_feature.created
        # sql_cmd = "SELECT USER_APELLATION FROM User WHERE USER_APELLATION = '%s'" % items_record.num  # 查询数据库
        # result = SQL('Web_Shop_User_DB',sql_cmd)  # 以元组形式返回匹配到的结果。
        for items_record in items_feature.record_array:
            print items_record.apellation, items_record.genre, items_record.num, items_record.created


# string = '1234567890123456789s'
# pattern = re.compile('^[A-Za-z0-9]{5,19}$')#大小写字母、数字、6-20位
# pattern = re.compile(u"^[\u4e00-\u9fa5A-Za-z0-9]{1,9}$")#大小写字母、数字、汉字、2-10位
# pattern = re.compile(u"^[\u4e00-\u9fa5A-Za-z]{1,4}$")#大小写字母、数字、汉字、2-4位
# pattern = re.compile('^[A-Za-z0-9].{5,19}$')#大小写字母、数字、字符 6-20位
# pattern = re.compile('^[a-zA-Z][a-zA-Z0-9_]{4,15}$')#大小写字母、数字、字符 6-20位
# result = pattern.findall(string.decode("utf-8"))
# print result[0]

# string = '你dsa'
# sss =string.decode("utf-8")
# if sss >= u"\u4e00" and sss <= u"\u9fa6":
    # print 'yes'
