list_ = [1,2,3,4,5,6,7,8,9]
tuple_ = (1,2,3,4,5,6,7,8,9)
# filter 第一个为传入的判断函数，一般是lambda函数，第二个为可迭代对象
# filter把可迭代对象的元素一个一个传入判断函数进行判断，如果为True就返回给（某种形式（如列表））变量
fn = list(filter(lambda x : x % 2 == 0,list_))
fnc = tuple(filter(lambda x : x % 2 == 0,tuple_))
print(fn,fnc)
"""
numbers = [1, 2, 3, 4, 5, 6]

# 使用lambda表达式和filter函数筛选出偶数
# 过滤函数 符合条件 保留 不符合删除
# 第一个参数是函数 第二个是传递的可迭代对象
even_numbers = filter(lambda num: num % 2 == 0, numbers)

# 将结果转换为列表并打印
print(list(even_numbers))  # 输出: [2, 4, 6]

"""