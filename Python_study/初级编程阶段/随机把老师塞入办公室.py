"""
使用列表嵌套，完成8名老师随机分配3个办公室。
提示：
定义一个列表存放8位老师
names = ['A','B','C','D','E','F','G','H']，
定义一个列表用来保存3个办公室offices = [[],[],[]]
"""
offices = [[],[],[]]
import random
names = ['A','B','C','D','E','F','G','H']
# 使用循环产生随机教室，再使用列表的操作把老师放进去
for i in names:
    ran_off = random.randint(0,2)
    offices[ran_off] += i
print(offices)