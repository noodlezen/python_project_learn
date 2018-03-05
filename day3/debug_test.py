#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import os
import sys


item_dict = {
    '1': {'iPhone': 60},
    '2': {'Mac': 120},
    '3': {'Food': 20},
    '4': {'Apple': 10},
    '5': {'pen': 5}
}

item_dict_2 = {
    '1': {'iPhone': 6000},
    '2': {'Mac': {'black': 120000}},
    '3': {'Food': 30},
    '4': {'Apple': 15},
    '5': {'pen': 10}
}

#函数:将字典转换为字符串，以' '和'\n'形式。参数：目标字典，目的字符串。返回值：字符串。
def dict_conver_str_recur(p_dict,p_str):
    if isinstance(p_dict,dict): #使用isinstance检测数据类型。
        for key in p_dict.iterkeys(): #用迭代器读取key，提高处理速度。
            value = p_dict[key]
            p_str += (str(key) + ' ') #以空格分割元素。
            if not isinstance(value,dict): #首层末尾添加换行符。
                p_str += (str(value) + '\n')
            p_str = dict_conver_str_recur(value,p_str) #带入返回值，自我调用实现递归遍历。
    return p_str

str_ss = ''
list_ss = []

str_ss = dict_conver_str_recur(item_dict_2,str_ss)
str_ss2 = str_ss[:-1]     #删除末尾1个字符


for i in str_ss2.split('\n'):
    list_ss.append(i)

print str_ss
print '=================='
print list_ss
print '=================='
#
