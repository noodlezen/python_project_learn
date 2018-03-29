#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    print 'MyTools模块以主程运行！ '
    # import __init__

import os
import random
import string
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import re
import md5

'''定义常量'''


'''定义类'''

class TextProces(object):
    __COLOR_MODE_DICT = {'d': 0, 'l': 1, 'u': 4, 'f': 5, 'r': 7, 'h': 8}
    __COLOR_UP_DICT = {'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'purple_red': 35, 'blue_blue': 36, 'white': 37
               }
    __COLOR_BACK_DICT = {'black': 40, 'red': 41, 'green': 42, 'yellow': 43, 'blue': 44, 'purple_red': 45, 'blue_blue': 46, 'white': 47
                 }
    __COLOR_ARGS_NUM = 2  # 读取额外的参数数量
    def __init__(self):
        pass

    def color(self, text, up_color='0', *args):
        mode = '0'
        back_color = '40'
        num = 0
        if up_color in TextProces.__COLOR_UP_DICT.iterkeys():
            up_color = str(TextProces.__COLOR_UP_DICT[up_color])
        elif up_color in TextProces.__COLOR_UP_DICT.itervalues():
            up_color = str(up_color)
        for var in args:
            num += 1
            if var in TextProces.__COLOR_MODE_DICT.iterkeys():
                mode = str(TextProces.__COLOR_MODE_DICT[var])
            elif var in TextProces.__COLOR_MODE_DICT.itervalues():
                mode = str(var)
            elif var in TextProces.__COLOR_BACK_DICT.iterkeys():
                back_color = str(TextProces.__COLOR_BACK_DICT[var])
            elif var in TextProces.__COLOR_BACK_DICT.itervalues():
                back_color = str(var)
            if num == TextProces.__COLOR_ARGS_NUM:
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
    __META_RULE_DICT = {
        '用户名': ('^[a-zA-Z][a-zA-Z0-9_]{4,15}$', '字母开头，允许大小写字母，数字，下划线组合，长度5-16字节。'),
        '用户密码': ('^(?=.*\d).{8,20}$', '用户密码必须以数字的组合，允许大小写字母，特殊字符。长度8-20字节。'),
        # '密码' : ('^(?=.*\d)(?=.*[a-zA-Z]).{8,20}$' , '密码必须以字母，数字的组合，允许特殊字符。长度8-20字节。'),
        # '密码' : ('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$' , '密码必须以大小写字母，数字的组合，允许特殊字符。长度8-20字节。'),
        '电子邮箱': ('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', '邮箱格式不合法！(xxxxxx@xxx.xx)')
    }
    def __init__(self):
        pass
    # 检测特征对象的数值是否符合规则。正确返回：True。 错误返回：错误信息。没有规则返回None。
    def check_meta_value(self, meta, value):
        pattern_array = TextRule.__META_RULE_DICT.get(meta)
        if pattern_array != None:
            pattern = re.compile(pattern_array[0])
            result = pattern.findall(value)  # .findall以列表形式返回
            if result:
                return True
            else:
                return pattern_array[1]
        else:
            return True


class Validate(object):
    __PWD = os.getcwd() #获取当前路径。
    __FATHER_PATH = os.path.abspath(os.path.dirname(__PWD)+os.path.sep+".")#获取当前父路径。
    __IMG_PATH = __PWD + '/temp/images/'
    __FONT_PATH = os.path.join(__FATHER_PATH, 'fonts/Ubuntu-R.ttf') #字体所在路径
    __CAPTCHA_NUM = 5 #验证码位数
    __IMG_SIZE = (100,30) #图片大小
    __IMG_BG_C = (255,255,255) #背景颜色白色
    __IMG_F_C = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) #字体颜色
    __IMG_L_C = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) #干扰线颜色
    # __IMG_F_C = (0,0,255) #字体颜色蓝色
    # __IMG_L_C = (255,0,0) #干扰线颜色红色
    __IMG_L_ON_OFF = True #干扰线开关
    __IMG_L_NUM = (1,5)
    # __SOURCE = list('1234567890') #纯数字
    __SOURCE = list(string.ascii_lowercase+'1234567890') #字母和数字

    def __init__(self):
        self.text_proces = TextProces()

    #生成随机字符串：
    def __generate_text(self):
        return ''.join(random.sample(Validate.__SOURCE,Validate.__CAPTCHA_NUM)) #调用字符串join方法插入空字符串

    #生成干扰线：
    def __genrate_line(self, draw, width, height):
        start = (random.randint(0,width), random.randint(0,height))
        end = (random.randint(0,width), random.randint(0,height))
        draw.line([start, end], fill = Validate.__IMG_L_C)

    #生成图片验证码：
    def __genrate_image_captcha(self):
        width,height = Validate.__IMG_SIZE #宽和高
        img = Image.new('RGBA', (width, height), Validate.__IMG_BG_C) #创建图片
        font = ImageFont.truetype(Validate.__FONT_PATH, 25) #设置字体
        draw = ImageDraw.Draw(img) #创建画笔
        text = self.__generate_text() #生成字符穿
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / Validate.__CAPTCHA_NUM, (height - font_height) / Validate.__CAPTCHA_NUM), text, font = font, fill = Validate.__IMG_F_C)

        if Validate.__IMG_L_ON_OFF:
            for i in range(5): #增加干扰线数量
                self.__genrate_line(draw, width, height)

        img = img.transform((width + 20, height + 10), Image.AFFINE, (1,-0.3,0,-0.1,1,0), Image.BILINEAR) #创建扭曲
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) #添加滤镜，边界加强

        img_file = text + '.png'
        img_path = os.path.join(Validate.__IMG_PATH,'%s'%img_file)
        img.save(img_path) #保存验证码图片
        img.show()
        return img_path, text

    def text_validate(self):
        text = self.__generate_text()
        # images = self.__genrate_image_captcha()
        print self.text_proces.color(text,'black','l','white')
        var = raw_input('请输入验证码:  ')
        if var == text:
            return True
        else:
            print self.text_proces.color('验证码错误请重新输入！','red','l')
            return False


'''定义函数'''

'''程序开始'''
# ob = Validate()
# ob.text_validate()
