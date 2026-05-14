my_list = [1,2,3,4,5,6,7,8]
iterator = iter(my_list)
#for 语句自动执行了先把可迭代对象转化为迭代器的操作，再使用next函数进行遍历
while True:
    try:
        print(next(iterator))
    except:
        break

