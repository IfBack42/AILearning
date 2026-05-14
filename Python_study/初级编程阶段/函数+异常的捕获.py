def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "除数不能为零"
    except TypeError:
        return "请输入数字类型的参数"




# def divide_numbers(a, b):
#     try:
#         result = a / b
#         return result
#     except (ZeroDivisionError, TypeError):
#         return "出现异常，异常可能为除数为零，或者类型错误"


# 示例调用
print(divide_numbers(10, 2))  # 正常情况，输出：5.0
print(divide_numbers(10, 0))  # 除数为零，输出："除数不能为零"
print(divide_numbers("10", 2))  # 参数类型错误，输出："请输入数字类型的参数"