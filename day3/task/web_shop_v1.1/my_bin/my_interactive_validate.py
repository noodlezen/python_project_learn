#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    print 'my_interactive_validate模块以主程运行！ '
    import __init__
import os
import random
import string
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from my_bin import my_proces_text

'''定义常量'''
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

#生成随机字符串：
def __generate_text():

    return ''.join(random.sample(__SOURCE,__CAPTCHA_NUM)) #调用字符串join方法插入空字符串

#生成干扰线：
def __genrate_line(p_draw, p_width, p_height):
    start = (random.randint(0,p_width), random.randint(0,p_height))
    end = (random.randint(0,p_width), random.randint(0,p_height))
    p_draw.line([start, end], fill = __IMG_L_C)

#生成图片验证码：
def __genrate_image_captcha():
    width,height = __IMG_SIZE #宽和高
    img = Image.new('RGBA', (width, height), __IMG_BG_C) #创建图片
    font = ImageFont.truetype(__FONT_PATH, 25) #设置字体
    draw = ImageDraw.Draw(img) #创建画笔
    text = __generate_text() #生成字符穿
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / __CAPTCHA_NUM, (height - font_height) / __CAPTCHA_NUM), text, font = font, fill = __IMG_F_C)

    if __IMG_L_ON_OFF:
        for i in range(5): #增加干扰线数量
            __genrate_line(draw, width, height)

    img = img.transform((width + 20, height + 10), Image.AFFINE, (1,-0.3,0,-0.1,1,0), Image.BILINEAR) #创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) #添加滤镜，边界加强

    img_file = text + '.png'
    img_path = os.path.join(__IMG_PATH,'%s'%img_file)
    img.save(img_path) #保存验证码图片
    # img.show()
    return img_path, text

def text_validate():
    while(True):
        text = __generate_text()
        print my_proces_text.color(text,'black','l','white')
        var = raw_input('请输入验证码:  ')
        if var == text:
            return True
        else:
            print my_proces_text.color('验证码错误请重新输入！','red','l')


# text_validate()
# __genrate_image_captcha()
# __genrate_color()
