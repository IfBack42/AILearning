# 定义一个函数，使用args/kwargs接收不定长参数
def func(*args, **kwargs):
    print(args)
    print(kwargs)


# 先定义变量，在传递参数
list1 = [10, 20, 30]
dict1 = {'num1': 40, 'num2': 50, 'num3': 60}

# 调用函数，传参
func(*list1, **dict1)