#!/usr/bin/env python
#_*_ coding:utf-8 _*_


lock_user_list = []

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

  #user_name = raw_input("请输入用户名:")
  #user_name = 'sss'
  #user_code = raw_input("请输入密码:")

  try:
    user_file = open(user_name + '.txt','r')
  except IOError:
    print "用户不存在!"

  else:
    
    if user_name in lock_user_list:
      print "该用户已锁定，请联系客服!"
      break

    else:

      user_code = raw_input("请输入密码:")

      user_file_line = user_file.readlines()
      user_file.close
  
      #user_file_len = len(user_file_line)
      flag = ''

      for line in user_file_line:
        temp_1 = line.strip('\n')
        flag = flag + temp_1
    
      print flag    
  
      if flag == ('id=' + user_name + 'code=' + user_code):
        print "登入成功!"
        break

      else:
        error_num += 1
        print "用户或密码错误!"
      
        if error_num >= 3:

          print "用户已锁定"

          try:
            lock_user = open('lock_user.txt','a')
          except IOError:
            print "黑名单打开错误!"
          else:
            lock_user.write(user_name + '\n')
            lock_user.close() 



