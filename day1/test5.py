#!/usr/bin/env python
#_*_ coding:UTF-8 _*_

name = raw_input('Please inpot your name:')
#age = raw_input('Age:')
#age = input('Age:')
job = raw_input('Job:')
salary = raw_input('Salary:')

real_age = 28

for i in range(10):
    age = input('age:')
    if age > 28:
        msg = 'think smalle!'
    elif age < 28:
        msg = 'think bigger!'
    else:
        print '\033[32;1m GOOD! 10 RMB \033[0m'
        break
    print msg
    print 'You still got %s shots!' % (9-i)

print type(age)

print '''
Personal information of %s:
    name: %s
    age: %d
    job: %s
    salary: %s
>>>>>>>>>>>>>>>>>>>>>>>>>>
''' % (name, name, age, job, salary)
