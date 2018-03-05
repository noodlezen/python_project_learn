#!/usr/bin/env python
#_*_ coding:utf-8 _*_

if __name__ == '__main__':
    import __init__

from Tkinter import *

from data import mysql
from bin import format_str

def test_1():
    pass

window_ob= Tk()
window_ob.title("33网络商城")
window_ob.geometry('800x600')
window_ob.resizable(width=False,height=True)

# test = Frame(height=200,width=300,bg='red').pack()

top_frm = Frame(window_ob,padx=5,pady=5)
Label(top_frm,bg='red',width=114,height=1).pack()
Button(top_frm,text="目录导航",command =test_1).pack(side=RIGHT)
Button(top_frm,text="购物车",command =test_1).pack(side=RIGHT)
Button(top_frm,text="我的设置",command =test_1).pack(side=RIGHT)

Button(top_frm,text="用户名",command =test_1).pack(side=LEFT)
top_frm.pack(side=TOP)


center_frm = Frame(window_ob)
Label(center_frm,bg='green',width=57,height=1).pack()
center_frm.pack(side=TOP)

# left_frm = Frame(window_ob)
# Label(left_frm,bg='green',width=57,height=30).pack()
# left_frm.pack(side=LEFT)

# right_frm= Frame(window_ob)
# Label(right_frm,bg='blue',width=57,height=30).pack()
# right_frm.pack(side=RIGHT)

login_frm =Frame(center_frm)
Label(login_frm,width=10,height=2, text='密码登入'.decode('utf8').encode('utf8'), font=('Arial',20)).pack()
login_frm.pack(side=TOP)

username_var = StringVar()
password_var = StringVar()

username_frm = Frame(login_frm)
Label(username_frm,width=30,height=1).pack(side=TOP)
username_entry = Entry(login_frm,width=25,textvariable = username_var).pack(side=TOP)
username_frm.pack(side=TOP)
password_frm = Frame(login_frm)
Label(password_frm,width=30,height=1).pack(side=TOP)
password_entry = Entry(login_frm,width=25,textvariable = password_var,show='*').pack(side=TOP)
password_frm.pack(side=TOP)
username_var.set("用户名")
password_var.set("密码")

Button(login_frm,text="提交",command = test_1).pack(side=TOP)

def test111():
    username = username_var.get()
    password = password_var.get()

    # Label(login_frm, text=username.decode('utf8').encode('utf8'), font=('Arial',20)).pack(side=TOP)

window_ob.mainloop()
