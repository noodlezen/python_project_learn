#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
# 用户账户ORM模块
# ORM: object relational mapping 对象-关系映射
# 把关系数据库的一行映射为一个对象，也就是一个类对应一个表
# ORM框架所有的类只能动态定义
'''

'''导入模块'''

import datetime
import re
import md5
from MyDateBase import *
from functools import wraps

'''装饰器'''
def field_option(func):
    # name: {name_cn, re_input, text_rule, encrypt}
    regist_option = {
            'user_name': {'name_cn': '用户名', 're_input': False, 'text_rule':('[a-zA-Z][a-zA-Z0-9_]{4,15}$', '必须以字母开头，允许大小写字母，数字，下划线组合，长度5-16字节。'), 'encrypt': False},
            'user_password': {'name_cn': '用户密码', 're_input': True, 'text_rule': ('^(?=.*\d).{8,20}$', '必须以数字的组合，允许大小写字母，特殊字符。长度8-20字节。'), 'encrypt': True},
            'user_email': {'name_cn': '用户邮箱', 're_input': False, 'text_rule': ('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', '格式不合法！(xxxxxx@xxx.xx)'), 'encrypt': False},
            'user_nicename': {'name_cn': '用户昵名', 're_input': False, 'text_rule': False , 'encrypt': False}
            }

    login_option = {
            'user_name': {'name_cn': '用户名', 're_input': False, 'text_rule': False , 'encrypt': False},
            'user_password': {'name_cn': '用户密码', 're_input': False, 'text_rule': False , 'encrypt': True}
            }
    @wraps(func)
    def inner(self, name, types, str_symbol, set_regist, set_login):
        # print func.__name__
        self.regist_option = set_regist
        self.login_option = set_login
        if self.regist_option:
            self.regist_option = regist_option[name]
        if self.login_option:
            self.login_option = login_option[name]
        func(self, name, types, str_symbol, set_regist, set_login)
    return inner


def sql_proces(func): #sql命令预处理装饰器
    @wraps(func)
    def inner(*args, **kw):
        field_names = [] # 数据库列名
        column_types = [] # 数据库列数据类型
        params = [] # 字符格式化符号参数
        names = [] # 实例属性名
        values = [] #实例属性值
        for items in args:
            if isinstance(items, object): #获取self
                my_instance = items # 元类定义的实例，比如User类
        for k, v in my_instance.__mappings__.items(): # 在所有映射中迭代,k是类属性名，v是类属性值
            # if hasattr(v, 'pattern'):
                # print k, v.pattern, v.explain
            field_names.append(v.name)
            column_types.append(v.types)
            params.append(v.str_symbol)
            names.append(k) # 类属性名同于实例属性名
            values.append(getattr(my_instance, k, None)) # 以类属性名,获取实例属性值。无定义类属性的实例属性的值设置为None
        func(my_instance, field_names, column_types, params, names, values)
    return inner


def singleton(cls): #单例装饰器
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance


'''定义类'''
# class FieldMetaclass(type):
    # def __new__(cls, *args, **kw):
        # print 'FieldMetaclass new'
        # return type.__new__(cls, *args, **kw)

# 定义Field(定义域：元类遇到Field的方法或属性时即进行修改）
class Field(object):
    _instance_count = 0

    @field_option
    def __init__(self, name, types, str_symbol, regist=False, login=False):  # 列名，列类型
        Field._instance_count += 1
        self.order = Field._instance_count #记录属性序号
        self.name = name
        self.types = types
        self.str_symbol = str_symbol

    def __str__(self):
        return "<%s:%s>" % (self.__class__.__name__, self. name)
        # 当用print打印输出的时候，python会调用他的str方法
        # 在这里是输出<类的名字，实例的name参数(定义实例时输入)>
        # 在ModelMetaclass中会用到
        # __class__获取对象的类，__name__取得类名

    def md5_encrypt(self, text):
        ob = md5.new()
        ob.update(text.encode("utf-8"))
        return ob.hexdigest()

    def input_value(self, name, repeat=False):
        input_var = raw_input("请输入%s:  " % name)
        if repeat:
            re_input_var = raw_input("请再次输入%s:  " % name)
            if input_var == re_input_var:
                self.value = input_var
                return True
            else:
                return '%s不一致，请重新输入！' % name
        self.value = input_var
        return True

    def check_textrule(self, text, text_rule):
        if text_rule:
            pattern = re.compile(text_rule[0])
            result = pattern.findall(text)
            if result:
                return True
            else:
                return text_rule[1]
        else:
            return True


class StringField(Field):
    def __init__(self, name, display_width=255, regist=False, login=False):
        super(StringField, self).__init__(name, 'VARCHAR(%d)' % display_width, "'%s'", regist, login)

class LongTextField(Field):
    def __init__(self, name, regist=False, login=False):
        super(LongTextField, self).__init__(name, "LONGTEXT", "'%s'", regist, login)

class IntField(Field):
    def __init__(self, name, display_width=11, regist=False, login=False):
        super(IntField, self).__init__(name, 'INT(%d)' % display_width, '%d', regist, login)

class IntegerField(Field):
    def __init__(self, name, display_width=20, regist=False, login=False):
        super(IntegerField, self).__init__(name, 'BIGINT(%d)' % display_width, '%u', regist, login)

class DateTimeField(Field):
    def __init__(self, name, regist=False, login=False):
        super(DateTimeField, self).__init__(name, "DATETIME", "'%s'", regist, login)


# 编写ModelMetaclass
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)
        # 如果说新创建的类的名字是Model，那直接返回不做修改
        print("Found model:%s" % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                # print ("Found mappings:%s ==> %s" % (k, v))  # 找到映射， 这里用到上面的__str__
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs["__mappings__"] = mappings
        attrs["__table__"] = name.lower()  # 添加表名，表名为类名的小写形式
        return type.__new__(cls, name, bases, attrs)

    #实现单例
    # _instances = {}
    # def __call__(cls, *args, **kwargs):
        # print ("Found instance:%s" % cls._instances)
        # if cls not in cls._instances:
            # cls._instances[cls] = super(ModelMetaclass, cls).__call__(*args, **kwargs)
        # return cls._instances[cls]

class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self,  **kw):
        super(Model, self).__init__(**kw) # 调用父类，即dict的初始化方法
        self.mysql = MySQL()
        self.__class_attr_order()

    def __getattr__(self, key): # 让获取key的值不仅仅可以d[k]，也可以d.k
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value): # 允许动态设置key的值，不仅仅可以d[k]，也可以d.k
        self[key] = value

    def __class_attr_order(self): #得到类属性顺序序列
        temp = dict()
        self.attr_order = list()
        for k, v in self.__mappings__.items():
            temp[v.order] = k
        for i in sorted(temp):
            self.attr_order.append(temp[i])


    @sql_proces
    def save(self, field_names, column_types, params, names, values):
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.__table__, ",".join(field_names), ",".join(params))
        for i in range(len(values)):
            if values[i] == None and params[i] != "'%s'":
                values[i] = 0
        sql = sql % tuple(values)
        # self.mysql.SQL(sql)
        print("SQL: %s" % sql)


    @sql_proces
    def load(self, field_names, column_types, params, names, values):
        key_values = []
        key_params = []
        for i in range(len(values)):
            if values[i] != None and type(values[i]) != datetime.datetime:
                key_values.append(getattr(self, names[i]))
                key_params.append("%s = %s" % (field_names[i], params[i]))
        sql = "SELECT %s FROM %s WHERE %s" % (",".join(field_names), self.__table__," AND ".join(key_params))
        for i in range(len(key_values)):
            if values[i] == None and params[i] != "'%s'":
                values[i] = 0
        print("SQL: %s" % sql)
        sql = sql % tuple(key_values)
        result = self.mysql.SELECT(sql)
        if result is not False:
            for i in range(len(names)):
                setattr(self, names[i], result[field_names[i]])
            return True
        else:
            return False

    @sql_proces
    def display(self, field_names, column_types, params, names, values):
        for name in names:
            print name, getattr(self, name)


    def regist(self):
        for k in self.attr_order: #按顺序取类属性名
            v = self.__mappings__[k]
            if v.regist_option is not False:
                while(True):
                    result = v.input_value(v.regist_option['name_cn'], v.regist_option['re_input'])
                    if result is True:
                        result = v.check_textrule(v.value, v.regist_option['text_rule'])
                        if result is True:
                            if v.regist_option['encrypt']:
                                v.value = v.md5_encrypt(v.value)
                            break
                        else:
                            print result
                    else:
                        print result
            if isinstance(v, DateTimeField):
                setattr(self, k, datetime.datetime.now())
            else:
                setattr(self, k, getattr(v, 'value', None))



class UserMeta(Model):
    ID = IntegerField("umeta_id")
    user_id = IntegerField("user_id")
    name = StringField("umeta_name")
    value = LongTextField("umeta_value")
    created = DateTimeField('umeta_created')

@singleton
class User(Model):
    ID = IntegerField("user_id")
    name = StringField("user_name", regist=True, login=True)
    password = StringField("user_password", regist=True, login=True)
    email = StringField("user_email", regist=True)
    nicename = StringField("user_nicename", regist=True)
    status = IntField("user_status")
    created = DateTimeField('user_created')

    def add_meta(self, name):
        nowtime = datetime.datetime.now()
        setattr(self, name, UserMeta(user_id=2, name=name, created=nowtime))




class Option(Model):
    ID = IntegerField("option_id")
    name = StringField("option_name")
    value = LongTextField("option_value")
    autoload = StringField("autoload")

# option = Option(name='user_regist', value='asd', autoload='yes')
# option.save()



# 创建一个实例
# u = User(name="mp4102")
# u.save()
