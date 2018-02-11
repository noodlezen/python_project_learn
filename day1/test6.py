#!/usr/bin/env python
#_*_ coding:utf-8 _*_

print_num = input("输入你要的循环次数(1-99):")
count = 0

while count < 100:

  if count == print_num:
    print "已经循环到:",count
    flag = raw_input("是否继续循环(y/n)")

    if flag == 'n':
      break
    else:
      while print_num <= count:
        print_num = input("输入你要的循环次数(1-99):")
        print "已经过了！"
    
  else:
    print "当前次数:",count

  count += 1

#else:
 # print "当前次数:",count


