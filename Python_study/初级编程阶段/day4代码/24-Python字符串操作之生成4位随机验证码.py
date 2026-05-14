'''
生成4位随机验证码，每次验证码都不同
要用到的知识点：随机数
mystr = 'abcdefg'
mystr[0]  # a
mystr[1]  # b
...
mystr[6]  # g
random.randint(0,6)
'''
# 导入random模块
import random

# 定义一个字符串（问题，怎么获取这个字符串的最大索引下标）
mystr = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"

# 编写循环结构，循环4次（需要几个字符就循环几次，因为每循环一次产生一个随机字符）
code = ''
for i in range(4):
    index = random.randint(0, len(mystr)-1)  # 0
    # print(mystr[index])
    code += mystr[index]                     # code += mystr[0]
# 输出生成的随机验证码
print(code)