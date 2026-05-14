# 导入turtle模块
import turtle
# 导入time模块
import time

# 设置画笔颜色
turtle.pencolor('red')
# 绘制五角星（一共五笔）
for i in range(5):
    turtle.forward(200)
    turtle.right(144)

# 休眠20s
time.sleep(20)