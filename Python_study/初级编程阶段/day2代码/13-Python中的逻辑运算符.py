'''
逻辑运算符 => and/or/not
'''
# 定义几个变量
num1 = 10
num2 = 6
num3 = 2

print((num1 > num2) and (num2 > num3))  # True and True => True
print((num1 < num2) or (num2 < num3))  # False or False => False
print(not (num1 > num2))  # not True => False（取反）

# 思考题
# print(3 and 4 and 5)  # 5
# print(5 and 6 or 7)   # 6
# 4 > 3 and print('hello world')  # hello world