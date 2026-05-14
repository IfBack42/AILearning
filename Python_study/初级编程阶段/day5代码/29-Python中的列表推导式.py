'''
1、创建一个列表，列表中包含0-9，10个元素
[0,1,2,3,...9]
range
'''
# list1 = []
# for i in range(10):
#     list1.append(i)
# print(list1)

# list1 = [i for i in range(10)]
# print(list1)


# 2、创建列表推导式，用于简化for循环与if语句
# 案例：生成0-9之间的偶数（i%2 == 0）序列
# list1 = []
# for i in range(10):
#     if i % 2 == 0:
#         list1.append(i)
# print(list1)

# list1 = [i for i in range(10) if i % 2 == 0]
# print(list1)

# 3、创建列表推导式，用于简化for嵌套结构
# 案例：创建列表 => [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
# 通过案例得出一个结论，外层循环1次，内层要循环3次
# range(1, 3)  =>  [1, 2]
# range(0, 3)  =>  [0, 1, 2]
list1 = []
for i in range(1, 3):
    for j in range(0, 3):
        list1.append((i, j))
print(list1)


list1 = [(i,j) for i in range(1, 3) for j in range(0, 3)]
print(list1)