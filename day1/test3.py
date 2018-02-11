#!/usr/bin/python3
# coding=utf-8
name = raw_input('Please inpot your name:')
# age = raw_input('Age:')
age = input('Age:')
job = raw_input('Job:')
salary = raw_input('Salary:')

print type(age)

print '''
Personal information usrof %s:
Name: %s
Age: %d
Job: %s
Salary: %s
 >>>>>>>>>>>>>>>>>>>>>>>>>>>
''' % (name, name, age, job, salary)
