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
import json
from MyDateBase import *
from MyTools import *
from functools import wraps

'''装饰器'''

def load_option(func):
    @wraps(func)
    def inner(self, *args, **kw):
        print 'Load option ---> %s' % func.__name__
        option = Options(name=func.__name__)
        if option.load():
            if option.autoload == 'yes':
                return func(self, option.value)
            else:
                return func(self, None)
        else:
            return False
    return inner

def sql_proces(func): #sql命令预处理装饰器
    @wraps(func)
    def inner(self, *args, **kw):
        field_names = [] # 数据库列名
        params = [] # 字符格式化符号参数
        indexs = [] # 数据库索引
        names = [] # 实例属性名
        values = [] #实例属性值
        index_values = []
        index_params = []
        for k in self.attr_order: #按顺序取类属性名
            v = self.__mappings__[k]
            field_names.append(v.name)
            params.append(v.str_symbol)
            indexs.append(v.index)
            names.append(k) # 类属性名同于实例属性名
            values.append(getattr(self, k, None)) # 以类属性名,获取实例属性值。无定义类属性的实例属性的值设置为None
        for i in range(len(values)):
            if indexs[i] != None and values[i] != None:
                if indexs[i] == 'PRIMARY KEY':
                    index_values = []
                    index_params = []
                    index_values.append(getattr(self, names[i]))
                    index_params.append("%s = %s" % (field_names[i], params[i]))
                    break
                else:
                    index_values.append(getattr(self, names[i]))
                    index_params.append("%s = %s" % (field_names[i], params[i]))

        return func(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw)
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

    def __init__(self, name, types, str_symbol, index):  # 列名，列类型, 格式化字符，索引
        Field._instance_count += 1
        self.order = Field._instance_count #记录属性序号
        self.name = name
        self.types = types
        self.str_symbol = str_symbol
        self.index = index

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
    def __init__(self, name, display_width=255, index=None):
        super(StringField, self).__init__(name, 'VARCHAR(%d)' % display_width, "'%s'", index)

class LongTextField(Field):
    def __init__(self, name, index=None):
        super(LongTextField, self).__init__(name, "LONGTEXT", "'%s'", index)

class IntField(Field):
    def __init__(self, name, display_width=11, index=None):
        super(IntField, self).__init__(name, 'INT(%d)' % display_width, '%d', index)

class IntegerField(Field):
    def __init__(self, name, display_width=20, index=None):
        super(IntegerField, self).__init__(name, 'BIGINT(%d)' % display_width, '%u', index)

class DateTimeField(Field):
    def __init__(self, name, index=None):
        super(DateTimeField, self).__init__(name, "DATETIME", "'%s'", index)


class ModelMetaclass(type): # 编写ModelMetaclass

    def __new__(cls, name, bases, attrs):
        if name == "Model": # 如果说新创建的类的名字是Model，那直接返回不做修改
            return type.__new__(cls, name, bases, attrs)
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
        self.validate = Validate()
        self.__class_attr_order()

    def __getattr__(self, key): # 让获取key的值不仅仅可以d[k]，也可以d.k
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value): # 允许动态设置key的值，不仅仅可以d[k]，也可以d.k
        self[key] = value

    # def __delattr__(self, key):
        # return self.pop(key)

    def __class_attr_order(self): #得到类属性顺序序列
        temp = dict()
        self.attr_order = list()
        for k, v in self.__mappings__.items():
            temp[v.order] = k
        for i in sorted(temp):
            self.attr_order.append(temp[i])

    @sql_proces
    def save(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):
        sql = "SELECT %s FROM %s WHERE %s" % (",".join(field_names), self.__table__," AND ".join(index_params))
        sql = sql % tuple(index_values)
        result = self.mysql.SELECT(sql)
        if result == False:
            print '-----insert-----'
            for i in range(len(values)): # 非字符数据写0
                if values[i] == None and params[i] != "'%s'":
                    values[i] = 0
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.__table__, ",".join(field_names), ",".join(params))
            sql = sql % tuple(values)
            print("SQL: %s" % sql)
            return self.mysql.SQL(sql)
        else:
            print '-----update-----'
            for i in range(len(values)):
                if values[i] != None:
                    if result[field_names[i]] != self[names[i]]:
                        up_values = []
                        up_values.append(self[names[i]])
                        sql = "UPDATE %s SET %s = %s WHERE %s" % (self.__table__, field_names[i], params[i], " AND ".join(index_params))
                        up_values.extend(index_values)
                        sql = sql % tuple(up_values)
                        print("SQL: %s" % sql)
                        return self.mysql.SQL(sql)


    @sql_proces
    def load(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):
        sql = "SELECT %s FROM %s WHERE %s" % (",".join(field_names), self.__table__," AND ".join(index_params))
        print("SQL: %s" % sql)
        sql = sql % tuple(index_values)
        result = self.mysql.SELECT(sql)
        if result is not False:
            for i in range(len(names)):
                setattr(self, names[i], result[field_names[i]])
            return True
        else:
            return False


    @sql_proces
    def delete(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):
        sql = "DELETE FROM %s WHERE %s" % (self.__table__," AND ".join(index_params))
        print("SQL: %s" % sql)
        sql = sql % tuple(index_values)
        return self.mysql.SQL(sql)


    @sql_proces
    def update_one(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):
        field_name, value = args[0], args[1] #函数形参
        up_values = []
        up_values.append(value)
        sql = "UPDATE %s SET %s = %s WHERE %s" % (self.__table__, field_name, params[field_names.index(field_name)], " AND ".join(index_params))
        up_values.extend(index_values)
        sql = sql % tuple(up_values)
        print("SQL: %s" % sql)
        return self.mysql.SQL(sql)


    @sql_proces
    def get_one(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):
        field_name = args[0] #函数形参
        sql = "SELECT %s FROM %s WHERE %s" % (field_name, self.__table__," AND ".join(index_params))
        print("SQL: %s" % sql)
        sql = sql % tuple(index_values)
        result = self.mysql.SELECT(sql)
        if result is not False:
            return result[field_name]
        else:
            return False


    @sql_proces
    def load_primary(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):
        for i in range(len(values)):
            if indexs[i] == 'PRIMARY KEY':
                primary_field_name = field_names[i]
                primary_name = names[i]
        sql = "SELECT %s FROM %s WHERE %s" % (primary_field_name, self.__table__," AND ".join(index_params))
        print("SQL: %s" % sql)
        sql = sql % tuple(index_values)
        result = self.mysql.SELECT(sql)
        if result is not False:
            setattr(self, primary_name, result[primary_field_name])
            return True
        else:
            return False


    @sql_proces
    def check_unique(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):
        for i in range(len(values)):
            if indexs[i] == 'UNIQUE' and values[i] != None:
                sql = "SELECT %s FROM %s WHERE %s = %s" % (field_names[i], self.__table__,field_names[i], params[i])
                sql = sql % values[i]
                result = self.mysql.SELECT(sql)
                if result != False:
                    print '%s已存在！' % field_names[i]
                    return False
        return True


    @sql_proces
    def display(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):
        for name in names:
            print name, getattr(self, name)



class Options(Model):
    ID = IntegerField("option_id", index='PRIMARY KEY')
    name = StringField("option_name", index='INDEX')
    value = LongTextField("option_value")
    autoload = StringField("autoload")

    def set(self, name, value, autoload):
        self.name = name
        self.value = value
        self.autoload = autoload

    @sql_proces
    def save(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.__table__, ",".join(field_names), ",".join(params))
        for i in range(len(values)):
            if values[i] == None and params[i] != "'%s'":
                values[i] = 0
            elif type(values[i]) is dict or type(values[i]) is list or type(values[i]) is tuple:
                values[i] = json.dumps(values[i]).replace('\\','\\\\') #填充\\以防mysql吃掉
        sql = sql % tuple(values)
        print("SQL: %s" % sql)
        self.mysql.SQL(sql)

    @sql_proces
    def load(self, field_names, params, indexs, names, values, index_values, index_params, *args, **kw):

        sql = "SELECT %s FROM %s WHERE %s" % (",".join(field_names), self.__table__," AND ".join(index_params))
        print("SQL: %s" % sql)
        sql = sql % tuple(index_values)
        result = self.mysql.SELECT(sql)
        if result is not False:
            for i in range(len(names)):
                if names[i] is 'value': # 还原json数据，并调用递归转码到utf-8
                    result[field_names[i]] = array_encode(json.loads(result[field_names[i]]))
                setattr(self, names[i], result[field_names[i]])
            return True
        else:
            return False


class UserMeta(Model):
    ID = IntegerField("umeta_id", index='PRIMARY KEY')
    user_id = IntegerField("user_id", index='INDEX')
    name = StringField("umeta_name", index='INDEX')
    value = LongTextField("umeta_value")
    created = DateTimeField('umeta_created')

class UserWrong(Model):
    ID = IntegerField("wrong_id", index='PRIMARY KEY')
    user_id = IntegerField("user_id", index='INDEX')
    name = StringField("wrong_name", index='INDEX')
    count = IntField("wrong_count")
    toplimit = IntField("wrong_toplimit")
    created = DateTimeField('wrong_created')
    expired = DateTimeField('wrong_expired')

    def check_duration(self):
        nowtime = datetime.datetime.now()
        return (self.expired - nowtime).total_seconds() + 10 if nowtime <= self.expired else False

    def check_count(self):
        return (self.toplimit - self.count) if self.count <= self.toplimit else False

    def count_add(self):
        self.count += 1


@singleton
class User(Model):
    ID = IntegerField("user_id", index='PRIMARY KEY')
    name = StringField("user_name", index='UNIQUE')
    password = StringField("user_password")
    email = StringField("user_email", index='UNIQUE')
    nicename = StringField("user_nicename", index='UNIQUE')
    status = IntField("user_status")
    created = DateTimeField('user_created')

    wrong_array = []

    def add_wrong(self, name, toplimit, duration):
        nowtime = datetime.datetime.now()
        expired = nowtime + datetime.timedelta(minutes=duration)
        self[name] = UserWrong(user_id=self.ID, name=name, count=1, toplimit=toplimit, created=nowtime, expired=expired)
        self.wrong_array.append(name)


    def load_wrong(self, name=None, wrong_id=None):
        if name!= None and wrong_id == None:
            if name in self.wrong_array:
                return self[name].load()
            else:
                self[name] = UserWrong(user_id=self.ID, name=name)
                self.wrong_array.append(name)
                return self[name].load()
        elif wrong_id != None:
            wrong = UserWrong(ID=wrong_id)
            if wrong.load():
                name = wrong.name
                self[name] = wrong
                return wrong
            else:
                return False
        else:
            return False

    def delete_wrong(self, name):
        if name in self.wrong_array:
            if self[name].delete():
                self.wrong_array.remove(name)
                self.pop(name) # 删除属性,等效delattr
                return True
            else:
                return False
        else:
            return False

    def check_status(self):
        result = self.get_one('user_status')
        return True if result == False else result

    def lock(self, wrong_id):
        self.status = wrong_id
        self.update_one('user_status', wrong_id)

    def unlock(self):
        self.status = 0
        self.update_one('user_status', 0)

    def input_info(self, option):
        for k in self.attr_order: #按顺序取类属性名
            v = self.__mappings__[k]
            if option != None:
                if v.name in option.iterkeys():
                    while(True):
                        result = v.input_value(option[v.name]['name_cn'], option[v.name]['re_input'])
                        if result is True:
                            result = v.check_textrule(v.value, option[v.name]['text_rule'])
                            if result is True:
                                if option[v.name]['encrypt']:
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

    @load_option
    def user_regist(self, option):
        self.input_info(option)
        self.display()
        if self.validate.text_validate():
            if self.check_unique():
                if self.save():
                    print '注册成功！'
                    result = True
                else:
                    print '注册失败！'
                    result = False
            else:
                result = False
        else:
            result = False
        return result


    @load_option
    def user_login(self, option):
        self.input_info(option)
        self.display()
        toplimit = 3
        duration = 2
        # if self.validate.text_validate():
        if True:
            if self.load_primary(): # 载入主键，user_id
                res1 = self.check_status()
                if res1 == True:
                    for k in self.attr_order: #按顺序取类属性名
                        v = self.__mappings__[k]
                        if v.name in option.iterkeys() and option[v.name]['encrypt'] == True:
                            res2 = self.get_one(v.name)
                            if self[k] == res2:
                                print 'right!'
                                wrong_name = v.name + '_wrong'
                                if self.load_wrong(wrong_name) == True: #载入错误
                                    self.delete_wrong(wrong_name) # 删除无效错误信息
                            else:
                                wrong_name = v.name + '_wrong'
                                if self.load_wrong(wrong_name) == False: #载入错误
                                    self.add_wrong(wrong_name, toplimit, duration) #添加错误
                                    self[wrong_name].save() # 保存到数据库
                                    print '%s错误！您还有%d次机会尝试！' % (v.name, toplimit - 1)
                                else:
                                    wrong = self[wrong_name]
                                    # wrong.display()
                                    remain_time = wrong.check_duration()
                                    if remain_time == False:
                                        self.delete_wrong(wrong_name) # 删除无效错误信息
                                        print '%s错误！您还有%d次机会尝试！' % (v.name, toplimit)
                                    else:
                                        wrong.count_add() # 增加错误次数
                                        remain_count = wrong.check_count()
                                        if remain_count == False:
                                            print '账户已锁定！%s错误次数超过限制,请在%d分钟后再次尝试登入！' % (v.name, int(remain_time / 60))
                                            self.lock(wrong.ID)
                                        else:
                                            print '%s错误！您还有%d次机会尝试！' % (v.name, remain_count)
                                        wrong.save()
                else:
                    wrong = self.load_wrong(wrong_id=res1) #载入错误
                    if isinstance(wrong, UserWrong):
                        wrong.display()
                        remain_time = wrong.check_duration()
                        if remain_time == False: #时间到解除锁定
                            self.delete_wrong(wrong.name) # 删除无效错误信息
                            self.unlock()
                            print '解除锁定，请重新登入'
                        else:
                            print '账户已锁定！%s错误次数超过限制,请在%d分钟后再次尝试登入！' % (wrong.name, int(remain_time / 60))
                    else:
                        print '有bug'

            else:
                print '用户不存在！'
                result = False
        else:
            print '验证码错误！'
            result = False



'''定义函数'''

def array_encode(array, code='utf-8'): #递归转换数组字典混合数据
    if isinstance(array, dict) == True:
        for k, v in array.items():
            if type(k) == unicode:
                array.pop(k)
                array[k.encode(code)] = v
            if isinstance(v, dict) == False and isinstance(v, list) == False:
                if type(v) == unicode:
                    v = v.encode(code)
                    array[k] = v
            else:
                array[k] = array_encode(v) #带入递归

    elif isinstance(array, list) == True:
        for i in range(len(array)):
            if isinstance(array[i], dict) == False and isinstance(array[i], list) == False:
                if type(array[i]) == unicode:
                    array[i] = array[i].encode(code)
            else:
                array[i] = array_encode(array[i]) #带入递归
    return array


'''程序开始'''

user_regist_option = {
            'user_name': {'name_cn': '用户名', 're_input': False, 'text_rule':['[a-zA-Z][a-zA-Z0-9_]{4,15}$', '必须以字母开头，允许大小写字母，数字，下划线组合，长度5-16字节。'], 'encrypt': False},
            'user_password': {'name_cn': '用户密码', 're_input': True, 'text_rule': ['^(?=.*\d).{8,20}$', '必须以数字的组合，允许大小写字母，特殊字符。长度8-20字节。'], 'encrypt': True},
            'user_email': {'name_cn': '用户邮箱', 're_input': False, 'text_rule': ['^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', '格式不合法！(xxxxxx@xxx.xx)'], 'encrypt': False},
            'user_nicename': {'name_cn': '用户昵名', 're_input': False, 'text_rule': False , 'encrypt': False}
            }

user_login_option = {
        'user_name': {'name_cn': '用户名', 're_input': False, 'text_rule': False , 'encrypt': False},
        'user_password': {'name_cn': '用户密码', 're_input': False, 'text_rule': False , 'encrypt': True}
        }


# option = Options(name='user_regist')

# ddd = option.load()
# if ddd == login_option:
    # print 'yes'
# elif ddd == regist_option:
    # print 'yes'

# print '==========================='
# option.set('user_login', user_login_option, 'yes')
# option.save()
# option.load()
# option.display()


# 创建一个实例
# u = User(name="mp4102")
# u.save()
