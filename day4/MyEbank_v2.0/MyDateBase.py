#!/usr/bin/env python
#_*_ coding:utf-8 _*_

# if __name__ == '__main__':
# print 'my_API_mysql.py以主程运行！ '
# import __init__

'''导入模块'''
import re
import MySQLdb
from MyTools import TextProces

'''定义常量'''
DB_HOST = 'localhost'
DB_USERNAME = 'noodlezen'
DB_PASSWORD = 'asd123'
DB_NAME = 'my_ebank'

'''定义类'''


class MySQL(object):
    def __init__(self):
        self.text_tools = TextProces()

    def SQL(self, cmd):
        db = MySQLdb.connect(DB_HOST, DB_USERNAME,
                             DB_PASSWORD, DB_NAME, charset='utf8')
        cursor = db.cursor()
        sql_cmd = cmd.split(' ')[0]
        try:
            cursor.execute(cmd)
            db.commit()
            if sql_cmd == 'SELECT':
                result = cursor.fetchall()
                # result = result.decode('utf-8').encode('gbk')
            else:
                result = True
            text = "MySQL数据库:%s, %s操作: 成功！" % (DB_NAME, sql_cmd)
            print self.text_tools.color(text, 'green', 'l')

        except:
            db.rollback()
            result = False
            text = "MySQL数据库:%s, %s操作: 失败！" % (DB_NAME, sql_cmd)
            print self.text_tools.color(text, 'red', 'l')
        db.close()
        return result

    def create_datebase(self, name):
        db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD)
        cursor = db.cursor()
        sql_cmd = "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8 COLLATE utf8_general_ci" % name
        try:
            cursor.execute(sql_cmd)
            result = True
            text = "数据库：%s 创建成功！" % name
            print self.text_tools.color(text, 'green', 'l')
        except:
            result = False
            text = "数据库：%s 创建失败！" % name
            print self.text_tools.color(text, 'red', 'l')
        db.close()
        return result

    def create_user_table(self):
        sql_cmd = "CREATE TABLE IF NOT EXISTS users (user_id BIGINT(20) PRIMARY KEY AUTO_INCREMENT, user_login VARCHAR(60) NOT NULL, user_genre VARCHAR(255), user_registered DATETIME NOT NULL) ENGINE=InnoDB AUTO_INCREMENT=2"
        return self.SQL(sql_cmd)

    def insert_user_table(self, ob):
        sql_cmd = "INSERT INTO users(user_login, user_genre, user_registered) VALUES ('%s','%s','%s')" % (ob.name, ob.genre, ob.created)
        return self.SQL(sql_cmd)

    def create_usermeta_table(self):
        sql_cmd = "CREATE TABLE IF NOT EXISTS usermetas (umeta_id BIGINT(20) UNSIGNED PRIMARY KEY AUTO_INCREMENT, user_id BIGINT(20) UNSIGNED NOT NULL, umeta_genre VARCHAR(255), umeta_name VARCHAR(100) NOT NULL, umeta_value LONGTEXT NOT NULL, umeta_types VARCHAR(60), umeta_status VARCHAR(100), umeta_modify INT(10) UNSIGNED, umeta_created DATETIME NOT NULL) ENGINE=InnoDB AUTO_INCREMENT=1"
        return self.SQL(sql_cmd)

    def insert_usermeta_table(self, user_id, ob):
        sql_cmd = "INSERT INTO usermetas(user_id, umeta_genre, umeta_name, umeta_value, umeta_types, umeta_status, umeta_modify, umeta_created) VALUES (%d, '%s', '%s', '%s', '%s', '%s', %d, '%s')" % (user_id, ob.genre, ob.name, ob.value, ob.types, ob.status, ob.modify, ob.created)
        return self.SQL(sql_cmd)

    def load_user_id(self, name):
        sql_cmd = "SELECT user_id FROM users WHERE user_login = '%s'" % name  # 查询数据库
        result = self.SQL(sql_cmd)
        return result[0][0] if result else False

    def check_user_exist(self, name):
        return True if self.load_user_id(name) else False
























'''old'''


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


def user_info_insert_mysql(p_db_name, p_ob):  # 把用户对象插入mysql数据库

    sql_cmd = "INSERT INTO User(USER_APELLATION, USER_GENRE, USER_CREATED) VALUES ('%s','%s','%s')" % (
        p_ob.apellation, p_ob.genre, p_ob.created)
    result = SQL(p_db_name, sql_cmd)  # 插入用户对象名，用户对象类型，创建时间，到数据库。

    for items_feature in p_ob.feature_array:  # 循环遍历用户对象的 属性信息。

        sql_cmd = "INSERT INTO User_Feature(USER_APELLATION, FEATURE_APELLATION, FEATURE_GENRE, FEATURE_MODIFIED_COUNT, FEATURE_CREATED) VALUES ('%s','%s','%s',%d,'%s')" % (
            p_ob.apellation, items_feature.apellation, items_feature.genre, items_feature.modified_count, items_feature.created)
        result = SQL(p_db_name, sql_cmd)  # 插入用户对象名，特征名，特征类型，修改次数，创建时间，到数据库。

        for items_record in items_feature.record_array:  # 循环遍历用户特征对象的 记录信息。

            sql_cmd = "INSERT INTO User_Feature_Record(USER_APELLATION, FEATURE_APELLATION, RECORD_APELLATION, RECORD_GENRE, RECORD_NUM, RECORD_CREATED) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                p_ob.apellation, items_feature.apellation, items_record.apellation, items_record.genre, items_record.num, items_record.created)
            # 插入用户对象名，特征名，记录名，记录类型，记录值，创建时间，到数据库。
            result = SQL(p_db_name, sql_cmd)


def user_load_record_mysql(p_db_name, p_username, p_feature):
    # 读出特征修改数
    sql_cmd = "SELECT FEATURE_MODIFIED_COUNT FROM User_Feature WHERE USER_APELLATION = '%s' AND FEATURE_APELLATION = '%s'" % (
        p_username, p_feature)  # 查询数据库
    result = SQL(p_db_name, sql_cmd)  # 以元组形式返回匹配到的结果。
    if len(result) != 0:
        if result[0][0] != 0:
            p_record = '当前记载'
        else:
            p_record = '初始记载'
        # 读出对应名称的记载值
        sql_cmd = "SELECT RECORD_NUM FROM User_Feature_Record WHERE USER_APELLATION = '%s' AND FEATURE_APELLATION = '%s' AND RECORD_APELLATION = '%s'" % (
            p_username, p_feature, p_record)  # 查询数据库
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
    sql_cmd = "SELECT WRONG_COUNT FROM User_Locked WHERE USER_APELLATION = '%s'" % p_ob.apellation  # 查询数据库
    result = SQL(p_db_name, sql_cmd)  # 以元组形式返回匹配到的结果。
    if len(result) == 0:  # 账户添加到名单,并记录错误次数，返回原因。
        wrong_count = 1
        reason = '密码错误！您还有%d次机会尝试登入！' % (p_toplimit - 1)
        result = p_ob.locked(p_db_name, reason, p_duration, wrong_count)
        if result == True:  # 锁定成功，返回理由
            return reason
        else:
            return False

    else:  # 累积错误次数，检查是否超时，更新原因
        wrong_count = result[0][0] + 1
        result = p_ob.check_lock_state(p_db_name)
        if result == True:  # 锁定时间到，解除锁定。
            result = p_ob.unlock(p_db_name)
            if result == True:
                result = '密码错误！您还有%d次机会尝试登入！' % p_toplimit
                return result
            else:
                return False
        else:  # 更新原因

            if wrong_count >= p_toplimit:  # 错误次数超出限额
                reason = '账户已锁定！登入密码错误次数超过限制,请在%d分钟后再次尝试登入！' % int(result / 60)
            else:
                reason = '密码错误！您还有%d次机会尝试登入！' % (p_toplimit - wrong_count)

            sql_cmd = "UPDATE User_Locked SET WRONG_COUNT = %d WHERE USER_APELLATION = '%s'" % (
                wrong_count, p_ob.apellation)  # 更新错误次数
            result = SQL(p_db_name, sql_cmd)
            sql_cmd = "UPDATE User_Locked SET REASON = '%s' WHERE USER_APELLATION = '%s'" % (
                reason, p_ob.apellation)  # 更新理由
            result = (result & SQL(p_db_name, sql_cmd))
            if result == True:  # 更新成功
                return reason
            else:
                return False


def user_locked_check(p_db_name, p_ob, p_toplimit):
    sql_cmd = "SELECT WRONG_COUNT FROM User_Locked WHERE USER_APELLATION = '%s'" % p_ob.apellation  # 查询数据库
    result = SQL(p_db_name, sql_cmd)  # 以元组形式返回匹配到的结果。
    if len(result) != 0:
        wrong_count = result[0][0]
        if wrong_count >= p_toplimit:  # 错误次数超过限制，检查锁定时间
            result = p_ob.check_lock_state(p_db_name)
            if result == True:  # 锁定时间到，解除锁定
                result = p_ob.unlock(p_db_name)
                return result
            else:  # 账户已被锁定，更新理由
                reason = '账户已锁定！登入密码错误次数超过限制,请在%d分钟后再次尝试登入！' % int(result / 60)
                sql_cmd = "UPDATE User_Locked SET REASON = '%s' WHERE USER_APELLATION = '%s'" % (
                    reason, p_ob.apellation)  # 更新理由
                result = SQL(p_db_name, sql_cmd)
                if result == True:
                    return reason
                else:
                    return False
        else:  # 错误次数不足，解除锁定,可正常登入
            result = p_ob.unlock(p_db_name)
            return result
    else:  # 账户没有被锁定,可正常登入
        return True

