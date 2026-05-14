# 导入time模块中的time方法
from time import time as t

# time.time()方法获取当前系统时间（起始时间）
start = t()

# 编写一个循环结构
list1 = []
for i in range(100000):
    list1.append(i)

# time.time()方法获取当前系统时间（结束时间）
end = t()

print(f'您的程序执行一共花费了{end - start:.2f}s时间')