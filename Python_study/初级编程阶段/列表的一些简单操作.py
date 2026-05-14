# 假设我们有一个存储商品价格的列表 prices，每个元素代表一个商品的价格。现在需要完成以下任务：
#
# 将价格列表按升序排序。
# 将价格列表反转，以得到降序排序的列表。
# 找到最高价格和最低价格。
# 计算所有商品的平均价格。

# 先遍历列表
prices = [22,13,124,41,525,142,52,76,345,86,96]
prices = sorted(prices)
# print(prices)
# # prices = list(reversed(prices))
# prices = prices[::-1]
# print(prices)
# 定义一个大哥，然后和其他元素打擂台
max = prices[0]
for i in prices:
    # 判断元素是否大于这个大哥
    if i > max:
        max = i
else:
    print(max)
min = prices[0]
for i in prices:
    if i < min:
        min = i
else:
    print(min)
# 要求平均价格，直接把列表求和再除以长度
sum = 0
lenth = len(prices)
for i in prices:
    sum += i
eval = sum / lenth
print(f"{eval:.2f}")