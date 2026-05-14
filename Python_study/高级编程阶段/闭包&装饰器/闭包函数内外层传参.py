"""
请完成如下函数 discount_calculator，用于生成商品折扣计算器，此计算器包含以下功能：

1，该函数接受一个参数 discount_rate，并返回一个闭包函数。

2，该闭包函数可以根据传入的商品价格计算折扣后的价格。

3，这个折扣计算器可以用于电商平台，用于生成一组特定折扣率的计算函数。
每个闭包函数都可以根据商品价格和特定的折扣率计算出折扣后的价格，方便在购物车结算时应用相应的折扣。

def discount_calculator(discount_rate):
    _______________________
        _______________________
        _______________________
    return calculate_discounted_price

# 创建折扣计算器
_______________________ = discount_calculator(90)
_______________________ = discount_calculator(80)

# 使用折扣计算器进行计算
price1 = 100
price2 = 50

discounted_price1 = ______________________________
discounted_price2 = ______________________________

print("打九折后的价格：", discounted_price1)
print("打八折后的价格：", discounted_price2)
"""
  #  函数闭包时外层函数参数在赋值时传入 第二个函数参数在调用时传入
def discount_calculator(discount_rate):
    def calculate_discounted_price(price):
        nonlocal discount_rate
        discounted_price = price * (discount_rate / 100)
        return discounted_price
    return calculate_discounted_price
discount_rate1 = 90
discount_rate2 = 80
price1 = 100
price2 = 50
discount_func1 = discount_calculator(discount_rate1)
discount_func1(price1)
print("打九折后的价格：", f"{discount_func1(price1)}")
discount_func2 = discount_calculator(discount_rate2)
discount_func2(price2)
print("打八折后的价格：", f"{discount_func2(price2)}")

