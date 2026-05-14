# 1、定义一个函数，用于生成指定长度的验证码
def generate_code(length):
    # 2、定义函数的说明文档
    '''
    generate_code函数主要用于生成指定长度的验证码
    :param length: int，代表生成验证码的长度
    :return: 返回指定长度的验证码
    '''
    code = ''
    str1 = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    # 使用循环生成指定长度的验证码
    import random
    for i in range(length):
        index = random.randint(0, len(str1) - 1)
        code += str1[index]
    # 设置一个返回值
    return code

# 3、调用generate_code函数
print(generate_code(6))