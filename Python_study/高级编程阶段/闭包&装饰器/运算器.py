"""
请完成如下函数 calculator_factory，用于生成计算器工厂函数。
1，该函数接受一个参数 operation，表示要进行的数学运算（加法、减法、乘法、除法），并返回一个闭包函数。
2，该闭包函数可以接收两个参数 num1 和 num2，并根据传入的操作进行相应的数学运算。

def calculator_factory(operation):
    if operation == "+":
        ____________________
            ____________________
        return add

    elif ____________________:
        ____________________
            ____________________
        return subtract

    elif ____________________:
        ____________________
            ____________________
        return multiply

    elif ____________________:
        ____________________
            ____________________
                ____________________
            ____________________
                ____________________
        return divide

# 创建加法计算器
add_calculator = calculator_factory("+")
result1 = add_calculator(5, 3)
print("加法计算结果：", result1)

# 创建减法计算器
subtract_calculator = calculator_factory("-")
result2 = subtract_calculator(8, 4)
print("减法计算结果：", result2)

# 创建乘法计算器
multiply_calculator = calculator_factory("*")
result3 = multiply_calculator(6, 2)
print("乘法计算结果：", result3)

# 创建除法计算器
divide_calculator = calculator_factory("/")
result4 = divide_calculator(10, 0)
print("除法计算结果：", result4)
"""
def calculator_factory(operation):
    if operation == "+":
        def add(num1,num2):
            return num1 + num2
        return add

    elif operation == "-":
        def subtract(num1,num2):
            return num1 - num2
        return subtract

    elif operation == "*":
        def multiply(num1,num2):
            return num1 * num2
        return multiply

    elif operation == "/":
        def divide(num1,num2):
            if num2 == 0:
                return False
            return num1 / num2
        return divide
add_calculator = calculator_factory("+")
result1 = add_calculator(5, 3)
print("加法计算结果：", result1)

subtract_calculator = calculator_factory("-")
result2 = subtract_calculator(8, 4)
print("减法计算结果：", result2)

multiply_calculator = calculator_factory("*")
result3 = multiply_calculator(6, 2)
print("乘法计算结果：", result3)

divide_calculator = calculator_factory("/")
result4 = divide_calculator(10, 0)
print("除法计算结果：", result4)