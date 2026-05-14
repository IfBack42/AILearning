# 定义一个变量name，用于接收商品的名称
name = input('请输入购买商品的名称：')
# 定义一个变量num，用于接收商品的编号
num = input('请输入购买商品的编号：')
# 定义一个变量price，用于接收商品的价格
price = float(input('请输入购买商品的价格：'))

# 使用print()函数进行格式化输出
print(f'您购买了{name}，商品编号为{num}，商品价格为{price * 2}，欢迎下次光临')