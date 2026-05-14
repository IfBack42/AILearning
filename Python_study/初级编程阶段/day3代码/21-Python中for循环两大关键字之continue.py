'''
continue:中止当前循环，继续下一次循环
'''
str1 = 'itheima'
for i in str1:
    if i == 'e':
        print('遇e不打印，中止本次循环，继续下一次循环')
        continue
    print(i)