# 定义一个列表
name_list = ['Tom', 'Rose', '二丫']
# 列表在计算机内存中，其存储结构与字符串类似，都是占用一段连续的内存地址
# 计算机的内存也会对列表中的每个元素进行编号，默认编号从0开始（索引下标）
# print(name_list[0])
# print(name_list[1])
# print(name_list[2])

# 遍历输出，一般和for循环结合使用
for i in name_list:
    # 列表中有多少个元素，则for循环就会自动循环多少次
    # 每次循环时，系统都会从列表中取出一个元素放入临时变量i中（变量i也可以叫其他名字，value）
    print(i)