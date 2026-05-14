'''
tuple() : 把其他序列类型转换为元组类型的数据
'''
# 定义一个列表
list1 = [10]
tuple1 = tuple(list1)
print(tuple1)

# 定义一个集合
set2 = {10, 20, 30, 40, 50}
tuple2 = tuple(set2)
print(tuple2)