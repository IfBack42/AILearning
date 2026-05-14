# 定义一个列表
name_list = ['Tom', 'Rose', 'Jennifer']
# 使用del方法删除索引为1的第2个元素
del name_list[1]
print(name_list)

# 定义一个列表
list1 = ['吕布', '貂蝉', '大乔']
# 使用pop()方法删除列表中的最后一个元素
del_name = list1.pop()
# del_name = list1.pop(1)  # 删除指定索引的那个元素
print(del_name)
print(list1)

# 定义一个列表
list2 = ['孙悟空', '白骨精', '兔子精']
# 使用remove()方法，删除元素值为'白骨精'的元素
list2.remove('白骨精')
print(list2)

# 定义一个列表
list3 = ['苹果', '香蕉', '番茄']
list3.clear()
print(list3)

# 定义一个空列表
empty_list = []