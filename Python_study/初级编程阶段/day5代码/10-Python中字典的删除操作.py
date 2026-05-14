# 定义一个字典
person = {'name':'关羽', 'age':35, 'mobile': 10086, 'address': '蜀国'}
# 删除字典中的某个key:value键值对（只需要指定key就可以了，因为key是唯一的）
del person['mobile']
print(person)

# clear()：用于清空字典中的所有key:value键值对
person.clear()
print(person)