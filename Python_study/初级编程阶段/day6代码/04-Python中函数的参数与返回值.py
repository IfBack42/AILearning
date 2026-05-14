# 案例三：升级案例二函数，可以实现向不同的人打不同的招呼
# def greet(name):
#     print('您好，' + name)

# 见到老张
# greet('老张')
# 见到老刘
# greet('老刘')
# 见到老王
# greet('老王')

# 案例四：函数的设计原则“高内聚、低耦合”，函数执行完毕后，应该主动把数返回给调用处，而不应该都交由print()等函数直接输出。
def greet(name):
    # 返回值（当greet函数执行完毕后，其会把返回值返回给函数的调用位置）
    return f'您好，{name}'

# 见到老张
print(greet('老张'))
# 见到老刘
print(greet('老刘'))
# 见到老王
print(greet('老王'))