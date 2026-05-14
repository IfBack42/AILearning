def sum_num(a, b):
    result = a + b
    print(result)
    # 强制中止函数的继续执行
    return None


print(sum_num(10, 20))  # None
# Python代码遵循顺序原则，从上往下一行一行执行
# 在函数中有两种情况，其返回值为None
# 第一种情况：如果一个函数没有返回值，则最终其return就是None
# 第二种情况：在函数体内部，直接打印return，由于没有指定返回值，默认也会返回None


