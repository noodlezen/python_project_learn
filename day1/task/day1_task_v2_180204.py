#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import os

print '''

	||========================||
	||<<<<<<<<欢迎光临>>>>>>>>||
	||>>>>>>>>登入接口<<<<<<<<||
	||========================||
	                      v2.0

'''
flag_1 = input("1.创建新用户\n2.用户登入\n请选择:")
flag_1_2 = 1

while flag_1_2 != 'n':
  if flag_1 == 1 :
    user_name = raw_input("请输入要创建的用户名:\n")
    user_code = raw_input("请输入要创建的密码:\n")

    if os.path.exists(user_name + '.txt'):
      flag_1_2 = raw_input("该用户已存在\n是否继续创建(y/n)?:")
    else:
      #print "创建文件夹"
      try:
        user_file = open(user_name + '.txt','w')
        #user_file.close()
      except IOError:
        print "文件打开错误！"
      else:
        user_file.write('id=' + user_name + '\n' + 'code=' + user_code)
        user_file.close()
      break

  else:
    break

lock_user_list = []
user_inf = []

try:
  lock_user = open('lock_user.txt','a')
  lock_user.close()
except IOError:
  print "找不到黑名单"
else:
  lock_user = open('lock_user.txt','r')
  lock_user_line = lock_user.readlines()
  lock_user.close
  for i in lock_user_line:
    line = i.strip('\n')
    lock_user_list.append(line)

#print len(lock_user_list)
#print lock_user_list[0]

error_num = 0

user_name = raw_input("请输入用户名:")

while error_num < 3:

  try:
    user_file = open(user_name + '.txt','r')
  except IOError:
    print "用户不存在!"
    break

  else:

    if user_name in lock_user_list:
      print "该用户已锁定，请联系客服!"
      break

    else:

      user_code = raw_input("请输入密码:")

      user_file_line = user_file.readlines()
      user_file.close

      for i in user_file_line:
        line = i.strip('\n')
        user_inf.append(line)

      if user_inf[0] == ('id=' + user_name) and user_inf[1] == ('code=' + user_code):
        print "登入成功!"
        print '''\033[32;1m 
        ||========================||
        ||>>>>>>>>登入成功<<<<<<<<||
        ||========================||
         \033[0m'''

        break

      else:
        error_num += 1
        print "用户或密码错误!还有%s次机会!" %(3-error_num)

        if error_num >= 3:

          print "用户已锁定"

          try:
            lock_user = open('lock_user.txt','a')
          except IOError:
            print "黑名单打开错误!"
          else:
            lock_user.write(user_name + '\n')
            lock_user.close()

