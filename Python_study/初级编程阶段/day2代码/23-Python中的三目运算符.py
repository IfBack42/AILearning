'''
基本语法：
语句段1 if 条件判断 else 语句段2
案例：求两个数的最大值
'''
num1 = 10
num2 = 20

# if num1 > num2:
#     print(f'最大值为{num1}')
# else:
#     print(f'最大值为{num2}')

max = num1 if num1 > num2 else num2
print(f'最大值为{max}')