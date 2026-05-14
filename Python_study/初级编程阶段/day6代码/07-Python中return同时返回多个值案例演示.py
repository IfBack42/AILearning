'''
定义一个函数，用于求两个数的四则运算结果（加、减、称、除）
'''
def calc(num1, num2):
    jia = num1 + num2
    jian = num1 - num2
    cheng = num1 * num2
    chu = num1 / num2
    return jia, jian, cheng, chu

# 调用calc函数
print(calc(10, 2))