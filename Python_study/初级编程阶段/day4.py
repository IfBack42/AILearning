name = "肖杰"
mobile = "10086"
print("我的名字是{},电话是{}".format(name, mobile))
print("我的名字是%s,电话是%s" % (name, mobile))
print(f"我的名字是{name},电话是{mobile}")

name2 = "wdnmd"
age = 33
number = 1
print(f"我的名字是{name2},今年{age}岁,我的学号是{number:06d}")
price = 1.98
print(f"大白菜今天{price:.2f}$/斤了！")
input(f"大白菜今天{price:.2f}$/斤了！")