"""
订单总金额计算

背景：假设你是一家电商平台的开发人员，需要编写一段代码来计算订单的总金额。

要求：给定一个字符串 order，其中包含多个订单信息，每个订单信息由商品名称、数量和价格组成，并以逗号分隔，计算订单的总金额。

注意事项：

数量是正整数。
价格是浮点数，保留两位小数。
订单信息之间用逗号 , 分隔。
order = "iPhone, 2, 6999.99, Macbook Pro, 1, 12999.99, iPad, 3, 3299.99"
"""
# 创建一个主的列表存放字典
main = []
# 把字符串变成列表
order = "iPhone, 2, 6999.99, Macbook Pro, 1, 12999.99, iPad, 3, 3299.99"
order = order.split(",")
sum = 0
# 把列表分割成数份字典，每三个元素装一个字典
i = 0
while i < len(order):
    part = {}
    part["name"] = order[i]
    i += 1
    part["num"] = int(order[i])
    i += 1
    part["price"] = float(order[i])
    i += 1
    main.append(part)
# 用每个字典的"num"键乘以“price”键再相加
for i in range(len(main)):
    sum = sum + main[i]["num"] * main[i]["price"]
print(sum)




