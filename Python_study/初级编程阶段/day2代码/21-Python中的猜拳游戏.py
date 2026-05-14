'''
游戏角色：player玩家   computer电脑
游戏规则：
石头-0，剪刀-1，布-2
① 玩家赢
player = 0, computer = 1
player = 1, computer = 2
player = 2, computer = 0
② 平局
③ 电脑赢
'''
# ① 导入random模块
import random

# 1、定义player玩家出拳信息
player = int(input('请输入您的出拳信息（石头-0，剪刀-1，布-2）：'))
# 2、定义computer电脑出拳信息
# ② 调用random模块中的randint方法
computer = random.randint(0, 2)

# 3、条件判断（使用if...elif...else多分支结构）
if (player == 0 and computer == 1) or (player == 1 and computer == 2) or (player == 2 and computer == 0):
    # 玩家赢
    print('玩家获胜')
elif player == computer:
    print('平局')
else:
    # 电脑赢
    print('电脑获胜')