#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Environment:Ubuntu_16.04_64
File:index.py
Description:
Author:NoodleZen <noodlezen@sina.com>
Created:2018.02.24
Maintainer:NoodleZen <noodlezen@sina.com>
Version:
Modified:2018.02.24
'''
from ipdb import set_trace
'''
from file import demo

print 'index',__name__
demo.foo()

if __name__ == '__main__':
    print 'is main file'
    pass

print __file__
print __doc__
'''

'''
def foo(name , action='eat' , where='beijin'):
    print name , 'go' , action , where

foo('xxx','ss')
foo('xxx')
foo('xxx','eat','beijin')
foo('xxx',action='beijin',where='eat')
'''

'''
def show_1(*args):
    print type(args)
    for item in args:
        print item

def show_2(**kargs):
    print type(kargs)
    for item in kargs.items():
        print item

user_dict = {'aaa':1,'bbb':2}

show_1('aaa','bbb','ccc')

show_2(name='aaa',age='bbb',job='ccc',email='ddd')
show_2(**user_dict)
'''

'''
set_trace()
#yield

def foo():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5

re = foo()
for item in re:
    print item
'''

'''
result = 'gt' if 1>3 else 'lt'
print result

temp = lambda x,y:x+y
print temp(2,4)
'''
'''
a = []
print dir()
print vars()
'''

'''
li = [11,22,33]
temp = map(lambda x:x+100,li)
print temp

temp = filter(lambda x:x<22,li)
print temp

temp = reduce(lambda x,y:x+y,li)
print temp

a = [1,2,3,4]
b = [3,1,3,4]
c = [2,8,3,4]
d = [7,9,3,4]
print zip(a,b,c,d)
'''

'''
a = '8*8'
b = '8+8'
c = '8-8'
d = '8%7'
e = '8/8'
print eval(a)
print eval(b)
print eval(c)
print eval(d)
print eval(e)
'''

'''
tmep ='sys'
func = 'path'
model = __import__(tmep)
print model.path
function = getattr(model,func)
print function
'''

'''
import random

# print random.random()
# print random.randint(1,5)
# print random.randrange(1,10)

code = []
for i in range(6):
    if i == random.randint(0,5):
        code.append(str(random.randint(0,9)))
    else:
        temp = random.randint(65,90)
        code.append(chr(temp))
print ''.join(code)
'''

'''
import hashlib

hash = hashlib.md5()
hash.update('admin')
print hash.hexdigest()
'''
import pickle

