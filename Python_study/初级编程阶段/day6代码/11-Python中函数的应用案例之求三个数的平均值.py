def avg_num(num1, num2, num3):
    '''
    avg_num函数主要用于返回三个数的平均值
    :param num1: int，第一个参数
    :param num2: int，第二个参数
    :param num3: int，第三个参数
    :return: 返回num1/num2/num3的平均值
    '''
    avg = (num1 + num2 + num3) / 3
    return avg

# 调用函数
print(avg_num(10, 20, 30))