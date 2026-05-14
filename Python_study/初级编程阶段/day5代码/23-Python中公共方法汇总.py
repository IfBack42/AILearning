'''
len() : 求数据序列的长度（个数）
del 序列名称[索引小标或者key] : 删除序列中指定的元素
'''
str1 = 'abcdefg'
print(len(str1))

list1 = [1, 2, 3, 4, 5]
print(len(list1))

dict1 = {'name':'Tom', 'age':23, 'mobile':'10086'}
print(len(dict1))

list2 = [1, 2, 3, 4, 5]
del list2[2]
print(list2)

dict2 = {'name':'Tom', 'age':23, 'mobile':'10086'}
del dict2['age']
print(dict2)