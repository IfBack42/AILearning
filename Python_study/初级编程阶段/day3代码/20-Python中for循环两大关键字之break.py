'''
break：中止整个循环结构
'''
str1 = 'itheima'
for i in str1:
    if i == 'e':
        print('遇e不打印，中止整个循环')
        break
    print(i)