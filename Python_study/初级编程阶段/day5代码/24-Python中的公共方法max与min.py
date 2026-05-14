'''
max() : 返回序列中的最大值
min() : 返回序列中的最小值
案例：输入3个数字，求3个数中最大值以及最小值
'''
num1 = int(input('请输入第一个数：'))
num2 = int(input('请输入第二个数：'))
num3 = int(input('请输入第三个数：'))

# 获取三个数的最大值
max_ = max(num1, num2, num3)
min_ = min(num1, num2, num3)

print(f'最大值：{max_}')
print(f'最小值：{min_}')

