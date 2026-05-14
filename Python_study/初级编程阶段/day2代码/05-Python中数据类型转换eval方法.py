# eval方法的作用：主要应用于字符串类型转换操作，将字符串的值转换为原数据类型
str1 = '10'
str2 = '9.99'

num1 = eval(str1)
print(num1)
print(type(num1))

num2 = eval(str2)
print(num2)
print(type(num2))