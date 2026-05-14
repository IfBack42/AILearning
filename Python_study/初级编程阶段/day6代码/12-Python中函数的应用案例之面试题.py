# 编写一个函数，有一个参数str1，输入信息如'1.2.3.4.5'，使用函数对其进行处理，要求最终的返回结果为'5-4-3-2-1'
def func(str1):  # 1.2.3.4.5
    '''
    func函数主要用于返回一个翻转后的字符串
    :param str1: 要翻转的字符串
    :return: 返回一个反转后的字符串
    '''
    # str1 = str1[::-1]
    # return str1.replace('.', '-')

    list1 = str1.split('.')
    list1.reverse()
    return '-'.join(list1)


# 调用函数
print(func('1.2.3.4.5'))  # 5-4-3-2-1