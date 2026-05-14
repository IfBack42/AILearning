import random
#先让电脑随机生成一个0——2之间的随机数
computer = random.randint(0,2)
#再让实体人输入一个数字
user = int(input("输入你要出的结果=>石头：0，剪刀：1，布：2:"))
#开始判断结果
if (user == 0 and computer == 1) or (user == 1 and computer == 2) or (user == 2 and computer == 0):
    print(f"你的结果是=>{user}，电脑的结果是{computer}，你赢了")
elif (user == 0 and computer == 0) or (user == 1 and computer == 1) or (user == 2 and computer == 2):
    print(f"你的结果是=>{user}，电脑的结果是{computer}，平局")
elif (user <0 or user > 2):
    print("瞎几把搞，飞起来")
else :
    print(f"你的结果是=>{user}，电脑的结果是{computer}，电脑赢了")