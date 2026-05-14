# 导入随机模块
import random

# 定义一个字符串
mystr = 'abcdefg'
# 返回字符串的长度
# print(len(mystr))
# 从以上mystr字符串中随机取出1个字符
# code1 = 'a'
# code2 = 'b'
# code = code1 + code2
# print(code)
code = ''
for i in range(4):
    num = random.randint(0, len(mystr) - 1)
    code += mystr[num]
print(code)


# print(mystr[0])
# print(mystr[1])
# print(mystr[2])
# print(mystr[3])
# print(mystr[4])
# print(mystr[5])
# print(mystr[6])