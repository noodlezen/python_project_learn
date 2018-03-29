#!/usr/bin/env python
#_*_ coding:utf-8 _*_

# if __name__ == '__main__':
# print 'my_API_mysql.py以主程运行！ '
# import __init__

'''导入模块'''
import re
import MySQLdb
import datetime
from MyTools import TextProces

'''定义常量'''
DB_HOST = 'localhost'
DB_USERNAME = 'noodlezen'
DB_PASSWORD = 'asd123'
DB_NAME = 'my_ebank_v3'

'''定义类'''


class MySQL(object):
    def __init__(self):
        self.text_proces = TextProces()

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
            print self.text_proces.color(text, 'green', 'l')

        except:
            db.rollback()
            result = False
            text = "MySQL数据库:%s, %s操作: 失败！" % (DB_NAME, sql_cmd)
            print self.text_proces.color(text, 'red', 'l')
        db.close()
        return result

    def SELECT(self, cmd):
        db = MySQLdb.connect(DB_HOST, DB_USERNAME,
                             DB_PASSWORD, DB_NAME, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute(cmd)
            db.commit()
            res_value = cursor.fetchall()
            print res_value
            res_field = cursor.description
            res_dict = {}
            for i in range(len(res_field)):
                value = res_value[0][i].encode(
                    'utf-8') if type(res_value[0][i]) == unicode else res_value[0][i]
                res_dict[res_field[i][0]] = value
            result = res_dict
            text = "MySQL数据库:%s, 获取字段名SELECT操作: 成功！" % DB_NAME
            print self.text_proces.color(text, 'green', 'l')

        except:
            db.rollback()
            result = False
            text = "MySQL数据库:%s, 获取字段名SELECT操作: 失败！" % DB_NAME
            print self.text_proces.color(text, 'red', 'l')
        db.close()
        return result
#--------------------创建类--------------------#

    def create_datebase(self, name):
        db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD)
        cursor = db.cursor()
        sql_cmd = "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8 COLLATE utf8_general_ci" % name
        try:
            cursor.execute(sql_cmd)
            result = True
            text = "数据库：%s 创建成功！" % name
            print self.text_proces.color(text, 'green', 'l')
        except:
            result = False
            text = "数据库：%s 创建失败！" % name
            print self.text_proces.color(text, 'red', 'l')
        db.close()
        return result

    def create_user_table(self):
        sql_cmd = "CREATE TABLE IF NOT EXISTS user (user_id BIGINT(20) PRIMARY KEY AUTO_INCREMENT, user_name VARCHAR(60) NOT NULL, user_password VARCHAR(255) NOT NULL, user_email VARCHAR(100) NOT NULL, user_nicename VARCHAR(100), user_status INT(10) UNSIGNED NOT NULL, user_created DATETIME NOT NULL) ENGINE=InnoDB AUTO_INCREMENT=2"
        return self.SQL(sql_cmd)

    def create_usermeta_table(self):
        sql_cmd = "CREATE TABLE IF NOT EXISTS usermeta (umeta_id BIGINT(20) UNSIGNED PRIMARY KEY AUTO_INCREMENT, user_id BIGINT(20) UNSIGNED NOT NULL, umeta_name VARCHAR(100) NOT NULL, umeta_value LONGTEXT NOT NULL, umeta_created DATETIME NOT NULL) ENGINE=InnoDB AUTO_INCREMENT=1"
        return self.SQL(sql_cmd)

    def create_userwrong_table(self):
        sql_cmd = "CREATE TABLE IF NOT EXISTS userwrong (wrong_id BIGINT(20) PRIMARY KEY AUTO_INCREMENT, user_id BIGINT(20) UNSIGNED NOT NULL, wrong_name LONGTEXT NOT NULL, wrong_count INT(10) UNSIGNED NOT NULL, wrong_toplimit INT(10) UNSIGNED NOT NULL, wrong_created DATETIME NOT NULL, wrong_expired DATETIME NOT NULL) ENGINE=InnoDB AUTO_INCREMENT=1"
        return self.SQL(sql_cmd)


'''
#--------------------插入类--------------------#

    def insert_user_table(self, name, genre, status, created):
        sql_cmd = "INSERT INTO users(user_name, user_genre, user_status, user_created) VALUES ('%s', '%s', %u, '%s')" % (
            name, genre, status, created)
        return self.__SQL(sql_cmd)

    def insert_usermeta_table(self, user_id, name, genre, value, types, modify, created):
        sql_cmd = "INSERT INTO usermeta(user_id, meta_name, meta_genre, meta_value, meta_types, meta_modify, meta_created) VALUES (%u, '%s', '%s', '%s', '%s', %u, '%s')" % (
            user_id, name, genre, value, types, modify, created)
        return self.__SQL(sql_cmd)

    def insert_userwrong_table(self, user_id, meta_id, name, genre, count, toplimit, created, expiry_date):
        sql_cmd = "INSERT INTO userwrong(user_id, meta_id, wrong_name, wrong_genre, wrong_count, wrong_toplimit, wrong_created, wrong_expiry_date) VALUES (%u, %u, '%s', '%s', %d, %d, '%s', '%s')" % (
            user_id, meta_id, name, genre, count, toplimit, created, expiry_date)
        return self.__SQL(sql_cmd)

#--------------------读取类--------------------#

    def xload_user(self, user_name=None, user_id=None):
        if user_id == None:
            sql_cmd = "SELECT * FROM users WHERE user_name = '%s'" % user_name
        else:
            sql_cmd = "SELECT * FROM users WHERE user_id = %u" % user_id
        return self.__SELECT(sql_cmd)

    def xload_usermeta(self, user_id=None, meta_name=None, meta_id=None):  # 获取数据表值和字段名，以字典返回
        if meta_id == None:
            sql_cmd = "SELECT * FROM usermeta WHERE user_id = %u AND meta_name = '%s'" % (
                user_id, meta_name)
        else:
            sql_cmd = "SELECT * FROM usermeta WHERE meta_id = %u" % meta_id
        return self.__SELECT(sql_cmd)

    def xload_userwrong(self, user_id=None, meta_id=None, wrong_id=None):  # 获取数据表值和字段名，以字典返回
        if wrong_id == None:
            sql_cmd = "SELECT * FROM userwrong WHERE user_id = %u AND meta_id = %u" % (
                user_id, meta_id)
        else:
            sql_cmd = "SELECT * FROM userwrong WHERE wrong_id = %u" % wrong_id
        return self.__SELECT(sql_cmd)

    def load_usermeta_id(self, user_id, meta_name):
        sql_cmd = "SELECT meta_id FROM usermeta WHERE user_id = %u AND meta_name = '%s'" % (
            user_id, meta_name)
        result = self.__SQL(sql_cmd)
        return result[0][0] if result else False

    def load_user_id(self, user_name):
        sql_cmd = "SELECT user_id FROM users WHERE user_name = '%s'" % user_name
        result = self.__SQL(sql_cmd)
        return result[0][0] if result else False

    # def load_user(self, user_name):
        # sql_cmd = "SELECT * FROM users WHERE user_name = '%s'" % user_name
        # result = self.__SQL(sql_cmd)
        # return result[0] if result else False

    # def load_usermeta(self, user_id, meta_name):
        # sql_cmd = "SELECT * FROM usermeta WHERE user_id = %u AND meta_name = '%s'" % (user_id, meta_name)
        # result = self.__SQL(sql_cmd)
        # return result[0] if result else False

    # def load_umeta_value(self, user_id, meta_id):
        # sql_cmd = "SELECT meta_value FROM usermeta WHERE user_id = %u AND meta_id = %u" % (user_id, meta_id)
        # result = self.__SQL(sql_cmd)  # 以元组形式返回匹配到的结果。
        # return result[0][0] if result else False

    # def load_ulocked_wrong_count(self, user_id, umeta_id):
        # sql_cmd = "SELECT wrong_count FROM userlocked WHERE user_id = %u AND umeta_id = %u" % (user_id, umeta_id)
        # result = self.__SQL(sql_cmd)
        # return result[0][0] if result else False

    def load_field(self, table):  # 获取数据表字段名，以列表返回
        db = MySQLdb.connect(DB_HOST, DB_USERNAME,
                             DB_PASSWORD, DB_NAME, charset='utf8')
        cursor = db.cursor()
        sql_cmd = "SELECT * FROM %s" % table
        try:
            cursor.execute(sql_cmd)
            db.commit()
            result = cursor.description
            field_name_list = []
            for field in result:
                field_name_list.append(field[0])
            result = field_name_list
            text = "MySQL数据库:%s, 获取字段名操作: 成功！" % DB_NAME
            print self.text_proces.color(text, 'green', 'l')

        except:
            db.rollback()
            result = False
            text = "MySQL数据库:%s, 获取字段名操作: 失败！" % DB_NAME
            print self.text_proces.color(text, 'red', 'l')
        db.close()
        return result

#--------------------更新类--------------------#

    def update_single(self, table, keys, keys_value, terms, terms_value):
        keys_value = ("'"+keys_value +
                      "'") if type(keys_value) == str else str(keys_value)
        terms_value = ("'"+terms_value +
                       "'") if type(terms_value) == str else str(terms_value)
        sql_cmd = "UPDATE %s SET %s = %s WHERE %s = %s" % (
            table, keys, keys_value, terms, terms_value)
        result = self.__SQL(sql_cmd)
#--------------------删除类--------------------#

    def delete_userwrong(self, wrong_id):
        sql_cmd = "DELETE FROM userwrong WHERE wrong_id = %u" % wrong_id
        return self.__SQL(sql_cmd)

#--------------------检查类--------------------#

#--------------------处理类--------------------#

#--------------------类--------------------#


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
'''
