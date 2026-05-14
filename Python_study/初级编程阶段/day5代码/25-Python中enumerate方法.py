'''
enumerate() ： 把字符串、列表、元组转换为key:value键值对结构
0:10
1:20
2:30
3:40
4:50
'''
list1 = [10, 20, 30, 40, 50]

# i = 0
# while i < len(list1):
#     print(f'{i}:{list1[i]}')
#     i += 1
#
# for i in list1:
#     print(i)
for key,value in enumerate(list1):
    print(f'{key}:{value}')