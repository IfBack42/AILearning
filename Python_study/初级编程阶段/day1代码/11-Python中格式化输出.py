'''
print()函数：主要功能用于实现对变量以及字符串类型数据的直接输出
完整写法
print(变量名称或要输出的文本信息, end='\n')
end参数，代表当前面的变量或文本信息输出完毕后，追加的内容，默认为\n，代表换行符
\转义字符
\t ：一个Tab键的缩进
\n ：换行符，实现自动换行（针对终端）
'''
# 定义一个变量name
name = '黑马程序员'
# 定义一个变量age
age = 23
# 定义一个家庭住址
address = '深圳市宝安区'

print(name, end='\t')
print(age, end='\t')
print(address, end='\t')