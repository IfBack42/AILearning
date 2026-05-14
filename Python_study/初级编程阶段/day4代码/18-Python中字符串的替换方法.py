# 定义一个字符串
str1 = 'hello linux'
# 使用replace方法对linux进行替换，替换为python
str2 = str1.replace('linux', 'python')
print(str2)

# 定义一个字符串
str3 = 'hello linux and hello linux'
# 使用replace方法对linux进行替换，替换为python（要求所有的linux都要进行替换）
print(str3.replace('linux', 'python', 1))