# 1、定义一个列表
list1 = ['刘备', '关羽', '赵云']
# 使用修改操作，将赵云这个元素修改为张飞
list1[2] = '张飞'
print(list1)

# 2、reverse倒叙排列
list2 = ['apple', 'banana', 'pear']
# list2.reverse()
# print(list2)
# 3、列表切片
print(list2[::-1])

# 4、使用sort对数据进行排序（主要针对数值居多）
list3 = [11, 33, 22, 18, 55]
# list3.sort()  # 从小到大
list3.sort(reverse=True)  # 从大到小
print(list3)