"""
假设你正在开发一个餐厅点餐系统，需要编写 Python 代码来处理订单信息和菜品库存。请完成以下要求：

创建一个函数place_order(table_number, *dishes, serving_time=None, **requirements)，用于记录订单信息和处理菜品库存。
参数 table_number 是位置参数，表示桌号。
参数 dishes 是不定长参数，表示顾客所点的菜品列表。
参数 serving_time 是关键字参数，表示就餐时间，默认为 None。
参数 requirements 是关键字参数，表示顾客对菜品的特殊要求。
在函数内部，根据菜品的库存数量和要求，判断是否能够满足顾客的点餐需求。
如果库存充足且满足要求，打印订单信息，并将对应菜品的库存数量减少；如果库存不足或不能满足要求，打印相应提示信息。
在主程序中，调用函数 place_order() 并传入相应的参数值，模拟一次实际点餐操作，并观察输出结果。
请编写上述要求的代码，并输出订单信息。

模拟菜品库存如下

menu = {
    '鱼香肉丝': 5,
    '宫保鸡丁': 3,
    '糖醋排骨': 0,
    '回锅肉': 4,
    '水煮鱼': 2
}
传递参数方式如下：

place_order(10, '鱼香肉丝', '宫保鸡丁', '糖醋排骨', '回锅肉', '水煮鱼', serving_time='19:00', 鱼香肉丝='少辣', 回锅肉='加蒜')
最终呈现结果为：

# 桌号：10
# 所点菜品：
#   - 鱼香肉丝
#     - 特殊要求：少辣
#   - 宫保鸡丁
#   - 糖醋排骨 点餐失败，该菜品不存在或库存不足
#   - 回锅肉
#     - 特殊要求：加蒜
#   - 水煮鱼
# 就餐时间：19:00
# 提示：
def demo(**requirements):
    if '鱼香肉丝' in requirements:
        print(requirements['鱼香肉丝'])
demo(鱼香肉丝='少辣')
"""
menu = {
    '鱼香肉丝': 5,
    '宫保鸡丁': 3,
    '糖醋排骨': 0,
    '回锅肉': 4,
    '水煮鱼': 2
}

def place_order(table_number, *dishes, serving_time=None, **requirements):
    global menu
    print(f"桌号：{table_number}")
    print("所点菜品：")
    for i in dishes: #dishes为元组，i为元组的元素
        for key,value in menu.items(): #menu为字典
            if i ==key and value == 0:
                print(f"    — {key} 点餐失败，该菜品库存不足或不存在")
                break
            elif i == key:
                menu[key] -= 1
                print(f"    — {key}")
                demo(i,**requirements)
                break
    print(f"就餐时间：{serving_time}")

def demo(i,**requirements): #这是一个存要求的字典
    for key,value in requirements.items():
        if i == key:
            print(f"    特殊要求 —{key}")

place_order(10, '鱼香肉丝', '宫保鸡丁', '糖醋排骨', '回锅肉', '水煮鱼', serving_time='19:00', 鱼香肉丝='少辣', 回锅肉='加蒜')
print(menu)