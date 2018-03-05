#!/usr/bin/env python
#_*_ coding:utf-8 _*_

__MODE_DICT = {
    'd': 0,
    'l': 1,
    'u': 4,
    'f': 5,
    'r': 7,
    'h': 8
}
__UP_DICT = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'purple_red': 35,
    'blue_blue': 36,
    'white': 37
}
__BACK_DICT = {
    'black': 40,
    'red': 41,
    'green': 42,
    'yellow': 43,
    'blue': 44,
    'purple_red': 45,
    'blue_blue': 46,
    'white': 47
}
__EX_P_NUM = 2 #读取额外的参数数量

if __name__ == '__main__':
    print 'format_str.py以主程运行！ '
    import __init__

import re
import md5

def color(p_str, p_up_color='0', *p_args):
    p_mode = '0'
    p_back_color = '40'
    num = 0

    if p_up_color in __UP_DICT.iterkeys():
        p_up_color = str(__UP_DICT[p_up_color])
    elif p_up_color in __UP_DICT.itervalues():
        p_up_color = str(p_up_color)

    for var in p_args:
        num += 1
        if var in __MODE_DICT.iterkeys():
            p_mode = str(__MODE_DICT[var])
        elif var in __MODE_DICT.itervalues():
            p_mode = str(var)
        elif var in __BACK_DICT.iterkeys():
            p_back_color = str(__BACK_DICT[var])
        elif var in __BACK_DICT.itervalues():
            p_back_color = str(var)

        if num == __EX_P_NUM:
            break

    result = '\033[' + p_mode + ';' + p_up_color + \
        ';' + p_back_color + 'm' + p_str + '\033[0m'
    return result


def xcolor(p_str, p_up_color=0, p_mode=0, p_back_color=40):

    p_mode = str(p_mode) if isinstance(p_mode, int) else str(__MODE_DICT[p_mode])
    p_up_color = str(p_up_color) if isinstance(
        p_up_color, int) else str(__UP_DICT[p_up_color])
    p_back_color = str(p_back_color) if isinstance(
        p_back_color, int) else str(__BACK_DICT[p_back_color]+10)

    result = '\033[' + p_mode + ';' + p_up_color + \
        ';' + p_back_color + 'm' + p_str + '\033[0m'
    return result


def encrypt_str(p_str):
    ob_m = md5.new()
    ob_m.update(p_str.encode("utf-8"))
    return ob_m.hexdigest()


def check_username_rule(p_str):#检查用户名命名规则
    main_pattern = re.compile('^[a-zA-Z][a-zA-Z0-9_]{4,15}$')#字母开头，允许大小写字母，数字，下划线组合，长度5-16字节
    result = main_pattern.findall(p_str.decode("utf-8"))
    if result:
        return True
    else:
        result = "用户名不合法！(以字母开头，允许大小写字母，数字，下划线组合，长度5-16字节。)"
        return result


def check_password_rule(p_str,p_level = 0):#检查密码命名规则。p_level参数密码强度，0:level_I, 2:level_II, 4:level_III
    level_pattern_array = [
            '^(?=.*\d).{8,20}$', "密码必须以数字的组合，允许大小写字母，特殊字符。长度8-20字节。",
            '^(?=.*\d)(?=.*[a-zA-Z]).{8,20}$', "密码必须以字母，数字的组合，允许特殊字符。长度8-20字节。",
            '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$', "密码必须以大小写字母，数字的组合，允许特殊字符。长度8-20字节。"
            ]
    pattern = re.compile(level_pattern_array[p_level])
    result =pattern.findall(p_str.decode("utf-8"))
    if result:
        return True
    else:
        result = level_pattern_array[p_level + 1]
        return result

def check_email_rule(p_str):#检查邮箱命名规则
    main_pattern = re.compile('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
    result = main_pattern.findall(p_str.decode("utf-8"))
    if result:
        return True
    else:
        result = "邮箱格式不合法！(xxxxxx@xxx.xx)"
        return result


string = 'rootss'

print encrypt_str(string)





