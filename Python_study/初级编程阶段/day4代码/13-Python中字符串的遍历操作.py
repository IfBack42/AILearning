'''
遍历操作：就是把序列类型的数据中的每一个元素，一个一个循环输出
'''
str1 = 'abcdefg'  #7个字符，索引下标最大值6

# 使用while循环
# 定义初始化计数器，由于字符串索引从0开始，所以i=0
i = 0
# 编写循环条件
while i < len(str1):
    print(str1[i])
    # 在循环体内部更新计数器的值
    i += 1

print('-' * 20)

# 使用for循环
for i in str1:
    print(i)