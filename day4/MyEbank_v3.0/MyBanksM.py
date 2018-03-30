#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''Bnak类模块'''
# if __name__ == '__main__':
# print 'error'

'''导入模块'''
import datetime
from MyAccountORM import *
from MyTools import *
from MyDateBase import *

'''定义常量'''

'''定义类'''

# class Singleton(type):
    # _instance = None
    # def __new__(cls, *args, **kw):
        # print args, kw
        # if not cls._instance:
            # cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        # return cls._instance

class MyBanks(object):
    # __metaclass__ = Singleton

    def __init__(self, *args):
        self.mysql = MySQL()

    def add_user(self, name):
        nowtime = datetime.datetime.now()
        self.user = User(name=name, created=nowtime)
        # self.ghost = Users(name='ghost', created=nowtime)
        # if type(self) is class:
            # print True

    # def load_user(self, name):
        # self.user = Users(name=name)
        # self.user.load()
        # self.user.display()

    # def save_user(self, name):
        # pass


bank = MyBanks()
# bank.mysql.create_user_table()
# bank.load_user('mp4102')
# ob = UserMeta(user_id=2)
# ob.load()



# bank.add_user('mp4102')
user = User()
# print user.__class__.__dict__
user.regist()
user.display()
user.save()
# bank.user.save()
# bank.user.load()
# bank.user.display()
# bank.user.add_meta('age')
# bank.user.age.save()
# bank.user.age.load()
# bank.user.age.display()
# bank.user.add_meta('phone')
# print bank.user is bank.ghost
# print bank.user.age is bank.user.phone
# print bank.user.phone
# bank.user.display()




class Basic(object):
    def __init__(self):
        self.text_rule = TextRule()
        self.text_proces = TextProces()
        self.validate = Validate()
        self.mysql = MySQL()

    # def load_user(self, user_name):
        # user_dict = self.mysql.xload_user(user_name)
        # if user_dict != False:
            # user_id = user_dict['user_id']
            # name = user_dict['user_name']
            # genre = user_dict['user_genre']
            # status = user_dict['user_status']
            # created = user_dict['user_created']
            # self.user = User(name, genre, user_id, status, created, user_dict)
            # return True
        # else:
            # return False

    def __input_info(self, keys):
        self.__input_var = raw_input("请输入%s:  " % keys)

    def print_info(self, text, color='0', *args):
        print self.text_proces.color(text, color, *args)

    # def display_user_info(self, user, meta_list):
        # for meta_name in meta_list:
            # if meta_name == '用户名':
                # print self.text_proces.color(
                    # meta_name + ':' + user.name, 'blue', 'l')
            # else:
                # meta = user.meta_dict.get(meta_name)
                # if meta_name != "用户密码":
                    # print self.text_proces.color(
                        # meta_name + ':' + meta.value, 'blue', 'l')


class Regist(Basic, object):
    def __init__(self):
        Basic.__init__(self)

    # def __add_ghost(self, ghost_name, genre=None):
        # self.ghost = User(ghost_name, genre)  # 创建零时用户对象

    def __input_info(self, meta_name):
        self.__input_var = raw_input("请输入%s:  " % meta_name)
        if meta_name == '用户密码':
            re_input_var = raw_input("请再次输入%s:  " % meta_name)
            if self.__input_var == re_input_var:
                result = self.text_rule.check_meta_value(
                    meta_name, self.__input_var)  # 调用文本规则检测
                if result == True:
                    self.__input_var = self.text_proces.encrypt(
                        self.__input_var)  # 给用户密码加密
                    return True
                else:
                    return result  # 返回错误信息
            else:
                return '用户密码不一致，请重新输入！'
        #不是密码直接调用文本规则检测
        return self.text_rule.check_meta_value(meta_name, self.__input_var)

    # def __insert_datebase(self, user):
        # if user.insert_datebase():  # 插入数据库
            # if user.get_id() != False:  # 获得数据库ID
                # for meta in user.meta_list:
                    # if not meta.insert_datebase(user.ID):  # 插入数据库
                        # return False
                # return True
            # else:
                # return False
        # else:
            # return False

    def regist_account(self, meta_list, meta_dict):
        for meta_name in meta_list:
            meta_types = meta_dict.get(meta_name)
            while(True):
                result = self.__input_info(meta_name)  # 调用内部输入方法，返回规则检测信息
                # if result == True:
                    # if meta_name == '用户名':
                        # self.__add_ghost(self.__input_var)
                        # break
                    # else:
                        # self.ghost.add_meta(
                            # meta_name, self.__input_var, meta_types)
                        # break
                # else:
                    # print self.text_proces.color(result, 'red', 'l')
        # self.display_user_info(self.ghost, meta_list)  # 显示注册信息
        # if self.validate.text_validate(): #调用验证码模块
            # if self.ghost.get_id() == False:
                # result = True if self.__insert_datebase(
                    # self.ghost) else False  # 注册信息插入数据库
            # else:
                # print self.text_proces.color('用户名已存在！', 'red', 'l')
                # result = False
        # else:
            # result = False
        # delattr(self, 'ghost')
        # return result


# class Login(Basic, object):
    # def __init__(self):
        # Basic.__init__(self)

    # def __add_ghost(self, ghost_name, genre=None):
        # self.ghost = User(ghost_name, genre)  # 创建零时用户对象

    # def __input_info(self, meta_name):
        # self.__input_var = raw_input("请输入%s:  " % meta_name)
        # if meta_name == '用户密码':
            # self.__input_var = self.text_proces.encrypt(
                # self.__input_var)  # 给用户密码加密

    # def __meta_worng_proces(self, user, toplimit, duration):
        # if not user.meta.load_wrong():  # 从数据库读取错误对象
            # name = '%s错误！您还有%d次机会尝试！' % (user.meta.name, toplimit - 1)
            # user.meta.add_wrong(name, '登入错误', toplimit, duration)  # 添加属性错误信息
            # user.meta.wrong.insert_datebase()  # 插入数据库
            # return name
        # else:
            # remain_time = user.meta.wrong.check_duration()  # 判断是否过期
            # if remain_time == False:
                # user.meta.delete_wrong()  # 删除无效错误信息
                # return '%s错误！您还有%d次机会尝试！' % (user.meta.name, toplimit)
            # else:
                # user.meta.wrong.modify_count(user.meta.wrong.count + 1)  # 累积次数
                # remain_count = user.meta.wrong.check_count()  # 检测剩余次数
                # if remain_count == False:  # 错误次数超出限额
                    # user.meta.wrong.modify_name('账户已锁定！%s错误次数超过限制,请在%d分钟后再次尝试登入！' % (
                        # user.meta.name, int(remain_time / 60)))  # 修改错误信息
                    # user.lock(user.meta.wrong.ID)  # 锁定用户对象
                    # result = user.meta.wrong.name
                # else:
                    # result = '%s错误！您还有%d次机会尝试！' % (
                        # user.meta.name, remain_count)
                # user.meta.wrong.update_datebase()  # 更新属性错误修改信息到数据库
                # user.update_datebase()  # 更新用户修改信息到数据库
                # return result

    # def login_account(self, meta_list, meta_dict):
        # result = True
        # for meta_name in meta_list:
            # meta_types = meta_dict.get(meta_name)
            # self.__input_info(meta_name)
            # if meta_name == '用户名':
                # self.__add_ghost(self.__input_var)
            # else:
                # self.ghost.add_meta(meta_name, self.__input_var, meta_types)
        # if self.validate.text_validate(): #调用验证码模块
            # for meta_name in meta_list:
                # if meta_name == '用户名':
                    # if self.load_user(self.ghost.name) == False:  # 从数据库读取用户
                        # self.print_info('用户名不存在！', 'red', 'l')
                        # result = False
                        # break
                    # else:
                        # result = self.user.check_status()  # 检测用户状态，返回Ture或错误id
                        # if result != True:
                            # self.user.load_wrong(wrong_id=result)  # 根据id读取错误对象
                            # remain_time = self.user.wrong.check_duration()  # 检测是否过期
                            # if remain_time == False:
                                # self.user.unlock()  # 用户解锁
                                # self.user.update_datebase()  # 用户对象更新数据库
                            # else:
                                # self.print_info('账户已锁定！请在%d分钟后再次尝试登入！' % int(
                                    # remain_time / 60), 'red', 'l')
                                # result = False
                                # break
                # else:
                    # __meta = self.ghost.meta_dict[meta_name]  # 获取零时用户属性对象
                    # self.user.load_meta(__meta.name)  # 从数据库读取用户属性
                    # if self.user.meta.cmp_value(__meta):  # 判断是否相等
                        # if self.user.meta.load_wrong():  # 读取是否有无效属性错误记录
                            # self.user.meta.delete_wrong()  # 删除无效错误记录
                        # res = True
                    # else:
                        # result = self.__meta_worng_proces(
                            # self.user, 3, 1)  # 调用密码错误处理
                        # if result != False:
                            # self.print_info(result, 'red', 'l')  # 输出错误信息
                        # res = False
                    # result = result and res
                    # if result == True:
                        # self.print_info('登入成功！', 'green', 'l')
        # else:
            # result = False
        # delattr(self, 'ghost')
        # return result

'''
class Rule(object):
    def __init__(self, name, pattern, explain):
        self.name = name
        self.pattern = pattern
        self.explain = explain

    def __str__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.explain)

class UsernameRule(Rule):
    def __init__(self, name):
        super(UsernameRule, self).__init__(name,'^[a-zA-Z][a-zA-Z0-9_]{4,15}$','字母开头，允许大小写字母，数字，下划线组合，长度5-16字节。')

class PasswordRule(Rule):
    def __init__(self, name):
        super(PasswordRule, self).__init__(name,'^(?=.*\d).{8,20}$','用户密码必须以数字的组合，允许大小写字母，特殊字符。长度8-20字节。')

class RuleModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "RuleModel":
            return type.__new__(cls, name, bases, attrs)
        print("Found model:%s" % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Rule):
                print ("Found mappings:%s ==> %s" % (k, v))  # 找到映射， 这里用到上面的__str__
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs["__mappings__"] = mappings
        # attrs["__table__"] = name.lower()  # 添加表名，表名为类名的小写形式
        return type.__new__(cls, name, bases, attrs)


class RuleModel(dict):
    __metaclass__ = RuleModelMetaclass

    def __init__(self,  **kw):
        super(RuleModel, self).__init__(**kw)
        self.mysql = MySQL()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'RuleModel' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def check(self):
        for k, v in self.__mappings__.items(): # 在所有映射中迭代,k是类属性名，v是类属性值
            print k
            print v.name, v.pattern, v.explain
            print getattr(self, k, None) # 以类属性名,获取实例属性值。无定义类属性的实例属性的值设置为None






class Regist(RuleModel):
    username = UsernameRule('user_name')
    password = PasswordRule('user_password')
    # email

# ob = Regist(username='mp4102',password='asd123')
# ob.check()

'''
