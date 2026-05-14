'''
函数调用，通过“键=值”形式加以指定。可以让函数更加清晰、容易使用，同时也清除了参数的顺序需求。
'''
def user_info(name, age, address):
    print(name)
    print(age)
    print(address)


# 使用关键字参数来传递参数
user_info(name='Tom', address='America', age=23)