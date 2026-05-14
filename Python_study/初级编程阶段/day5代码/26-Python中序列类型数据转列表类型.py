# 1、定义一个元组
tuple1 = (10, 20, 30)
# 2、将其转换为列表形式
list1 = list(tuple1)
print(list1)


# 2、定义一个集合
set2 = {'apple', 'banana', 'pear'}
list2 = list(set2)
print(list2)


# 3、定义一个字典，将其转换为列表类型 => 只能把key作为列表的元素，value会自动舍弃
dict3 = {'name':'Tom', 'age':23, 'address': '深圳市宝安区'}
list3 = list(dict3)
print(list3)