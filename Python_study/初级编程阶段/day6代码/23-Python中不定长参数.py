# 案例：求函数所有参数的和（参数数量不固定）
# 结果 = 10 + 20 + 30 + 40 + 50
def func(*args, **kwargs):
    result = 0
    # 既能接收元组类型的数据，也可以字典类型的数据
    # print(args)
    for i in args:
        result += i
    # print(kwargs)
    for i in kwargs.values():
        result += i
    return result


print(func(10, 20, 30, num1=40, num2=50))