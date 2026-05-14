# 1、把字符串类型的数据转化为int整数类型
# num = int(input('请输入您的幸运数字：'))
#
# print(num)
# print(type(num))

# 2、把int整数类型转换为float浮点类型
# num = 10
# print(num)
# print(type(num))
#
# print('-' * 20)
#
# num = float(num)
# print(num)
# print(type(num))

# 3、把float浮点类型转换为int整数类型
# num = 10.88
# print(num)
# print(type(num))
#
# print('-' * 20)
#
# num = int(num)  # 如果把浮点类型的数据转换为整型数据，则小数点后的数据会丢失！！！
# print(num)
# print(type(num))

# 4、把字符串类型的数据转为数值类型
str1 = '10'
str2 = '10.88'

num1 = int(str1)
num2 = float(str2)

print(type(num1))
print(type(num2))
