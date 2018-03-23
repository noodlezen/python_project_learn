#!/usr/bin/env python
# -*- coding: utf-8 -*-

' Simple ORM using metaclass '

from MyTools import *
tools = TextProces()

class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k, v in attrs.iteritems():
            print tools.color(str(k),'green','l'), type(k)
            print tools.color(str(v),'green','l'), type(v)
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)

class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        print args
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

# testing code:

class UserMeta(Model):
    meta_id = IntegerField('meta_id')
    meta_name = StringField('meta_username')
    # meta_email = StringField('meta_email')
    # meta_password = StringField('meta_password')

class User(Model):
    id = IntegerField('uid')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')
    # usermeta = UserMeta(meta_id=222, meta_name='phone')

    # def add_usermeta(self,p_meta_id, p_meta_name):
        # self.usermeta = UserMeta(meta_id=p_meta_id, meta_name=p_meta_name)

# setattr(User,'phone',StringField('phone'))
u = User(id=12345, name='Noodlezen', email='noodlezen@sina.com', password='asd123')
# u.add_usermeta(222,'phone')
setattr(u,'phone',UserMeta(meta_id=222, meta_name='phone'))
setattr(u,'age',UserMeta(meta_id=16, meta_name='age'))
# print User.phone
# User.__metaclass__()


u.save()
print '+++++++++++++++++++++++++++++++++++++++'
# u.usermeta.save()
# u.phone.save()
# u.age.save()
meta_list = ['phone','age']
for usermeta in meta_list:
    getattr(u, usermeta, None).save()

