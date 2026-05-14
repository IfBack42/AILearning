'''
在Python代码中，理论上一个函数只能返回一个值，但是我们可以借助tuple元组同时返回多个值
'''
def return_num():
    return 1, 2

# 调用return_num函数
print(return_num())
print(type(return_num()))