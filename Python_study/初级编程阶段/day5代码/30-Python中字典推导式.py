'''
案例1：创建一个字典：字典key是1-5数字，value是这个数字的2次方。
dict1 = {1:1, 2:4, 3:9, 4:16, 5:25}
'''
# dict1 = {i:i**2 for i in range(1, 6)}
# print(dict1)

'''
案例2：
list1 = ['name', 'age', 'gender']
list2 = ['Tom', 20, 'male']
# 结果：person = {'name':'Tom', 'age':20, 'gender':'male'}
'''
list1 = ['name', 'age', 'gender']
list2 = ['Tom', 20, 'male']
person = {list1[i]:list2[i] for i in range(3)}
print(person)

'''
案例3：
counts = {'MBP': 268, 'HP': 125, 'DELL': 201, 'Lenovo': 199, 'ACER': 99}
需求：提取上述电脑数量大于等于200的字典数据
newdict = {'MBP': 268, 'DELL': 201}
'''
counts = {'MBP': 268, 'HP': 125, 'DELL': 201, 'Lenovo': 199, 'ACER': 99}
newdict = {key:value for key, value in counts.items() if value >= 200}
print(newdict)