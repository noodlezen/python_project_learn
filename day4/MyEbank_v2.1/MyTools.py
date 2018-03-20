#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    print 'MyTools模块以主程运行！ '
    # import __init__

import re
import md5

'''定义常量'''

MODE_DICT = {'d': 0, 'l': 1, 'u': 4, 'f': 5, 'r': 7, 'h': 8}
UP_DICT = {'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'purple_red': 35, 'blue_blue': 36, 'white': 37
           }
BACK_DICT = {'black': 40, 'red': 41, 'green': 42, 'yellow': 43, 'blue': 44, 'purple_red': 45, 'blue_blue': 46, 'white': 47
             }
EX_P_NUM = 2  # 读取额外的参数数量

# 属性规则
meta_RULE_DICT = {
    '用户名': ('^[a-zA-Z][a-zA-Z0-9_]{4,15}$', '字母开头，允许大小写字母，数字，下划线组合，长度5-16字节。'),
    '用户密码': ('^(?=.*\d).{8,20}$', '用户密码必须以数字的组合，允许大小写字母，特殊字符。长度8-20字节。'),
    # '密码' : ('^(?=.*\d)(?=.*[a-zA-Z]).{8,20}$' , '密码必须以字母，数字的组合，允许特殊字符。长度8-20字节。'),
    # '密码' : ('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$' , '密码必须以大小写字母，数字的组合，允许特殊字符。长度8-20字节。'),
    '电子邮箱': ('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', '邮箱格式不合法！(xxxxxx@xxx.xx)')
}

'''定义类'''

class TextProces(object):
    def __init__(self):
        pass

    def color(self, text, up_color='0', *args):
        mode = '0'
        back_color = '40'
        num = 0
        if up_color in UP_DICT.iterkeys():
            up_color = str(UP_DICT[up_color])
        elif up_color in UP_DICT.itervalues():
            up_color = str(up_color)
        for var in args:
            num += 1
            if var in MODE_DICT.iterkeys():
                mode = str(MODE_DICT[var])
            elif var in MODE_DICT.itervalues():
                mode = str(var)
            elif var in BACK_DICT.iterkeys():
                back_color = str(BACK_DICT[var])
            elif var in BACK_DICT.itervalues():
                back_color = str(var)
            if num == EX_P_NUM:
                break
        result = '\033[' + mode + ';' + up_color + \
            ';' + back_color + 'm' + text + '\033[0m'
        return result

    def encrypt(self, text):
        ob = md5.new()
        ob.update(text.encode("utf-8"))
        return ob.hexdigest()

    def get_types(self, text):
        return str(type(text)).strip("<>").strip("type ").strip("'")


class TextRule(object):
    def __init__(self):
        pass
    # 检测特征对象的数值是否符合规则。正确返回：True。 错误返回：错误信息。没有规则返回None。
    def check_meta_value(self, meta, value):
        pattern_array = meta_RULE_DICT.get(meta)
        if pattern_array != None:
            pattern = re.compile(pattern_array[0])
            result = pattern.findall(value)  # .findall以列表形式返回
            if result:
                return True
            else:
                return pattern_array[1]
        else:
            return True


'''定义函数'''

'''程序开始'''
