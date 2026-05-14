# 1、定义两个数的加和
def add_num(num1, num2):
    return num1 + num2

# 2、定义两个数的相减
def sub_num(num1, num2):
    return num1 - num2

# 3、在当前文件中直接调用相关功能进行测试
# print(__name__)  # 当前文件运行结果 => __main__

if __name__ == '__main__':
    print(add_num(10, 20))
