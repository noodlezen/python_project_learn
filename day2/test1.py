#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''
a = range(10)
b = range(10)

a = [str(i) for i in a]

print a

for i in b:
  b[i] = str(i)

print b
'''
f = file('sss.txt','r')
for i in f.readlines():
  print i.strip('\n').split(':')
