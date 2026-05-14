'''
所谓的赋值运算符就是我们日常生活中的等号，但是在Python代码中，=代表赋值运算符。其功能代表把等号右边的计算机结果赋值给左边的变量
'''
# 1、单个变量赋值
num = 10
print(num)

# 2、多个变量同时赋值（元组拆包）
num1, str1, bool1 = 10, 'hello world', True
print(num1)
print(str1)
print(bool1)

# 3、为多个变量赋予相同的值
a = b = 19.98
print(a)
print(b)