# 导入pygame模块
import pygame
# 导入time模块
import time
# 导入pygame.locals模块
from pygame.locals import *

# 定义英雄飞机横坐标
hero_x = 150
# 定义英雄飞机纵坐标
hero_y = 600

#a 定义英雄飞机的弹仓
my_bullet = []

# 加载飞机爆炸的多张图片（按照顺序）
a = pygame.image.load('feiji/enemy2_down1.png')
b = pygame.image.load('feiji/enemy2_down2.png')
c = pygame.image.load('feiji/enemy2_down3.png')
d = pygame.image.load('feiji/enemy2_down4.png')
e = pygame.image.load('feiji/enemy2_down5.png')
f = pygame.image.load('feiji/enemy2_down6.png')

# 定义一个列表（爆炸）
blow_up = [a, b, c, d, e, f]

# 定义一个变量enemy_life
enemy_life = 'live'  # live存活，dead死亡

# 定义enemy_x（敌机的横坐标）
enemy_x = 130
enemy_path = 'right'
enemy_num = 0  # 初始值为0，代表加载爆炸的第一张图片，循环时，依次累加，但是不能超过6

# 定义一个函数enemy_plane
def enemy_plane(screen, enemy):
    # 声明全局变量
    global enemy_x
    global enemy_path
    global enemy_life
    global enemy_num

    # 最终代码 => 子弹击中飞机，则飞机enemy_life切换dead状态
    for bullet in my_bullet:
        # 遍历所有子弹的坐标，判断是否有子弹击中飞机
        if (bullet['x'] >= enemy_x and bullet['x'] <= enemy_x + 165) and (bullet['y'] >= 0 and bullet['y'] <= 256):
            # 击中飞机
            enemy_life = 'dead'

    if enemy_life == 'live':
        # 粘贴敌方飞机
        screen.blit(enemy, (enemy_x, 10))

        # 添加一个判断语句（防止飞机越界）
        if enemy_x >= 235:
            enemy_path = 'left'
        elif enemy_x <= 0:
            enemy_path = 'right'

        # 根据设置的方向让飞机移动起来
        if enemy_path == 'left':
            enemy_x -= 10
        elif enemy_path == 'right':
            enemy_x += 10
    elif enemy_life == 'dead':
        if enemy_num <= 5:
            screen.blit(blow_up[enemy_num], (enemy_x, 10))
            enemy_num += 1


# 定义一个函数hero_plane
def hero_plane(screen, hero, bullet):
    # 声明全局变量
    global hero_x
    global hero_y

    # 飞机如何移动？理论就是捕获键盘事件，然后获取上下左右按键，然后移动图片的横纵坐标
    screen.blit(hero, (hero_x, hero_y))

    # 获取pygame键盘按下事件，pygame.event.get()获取所有事件，返回结果是一个列表
    for event in pygame.event.get():
        if event.type == QUIT:
            # 退出游戏
            exit()
        # KEYDOWN键盘按下事件
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                hero_y -= 10
            elif event.key == K_DOWN:
                hero_y += 10
            elif event.key == K_LEFT:
                hero_x -= 10
            elif event.key == K_RIGHT:
                hero_x += 10
            elif event.key == K_SPACE:
                print('发生子弹')
                my_bullet.append({'x': hero_x + 32, 'y': hero_y - 40})
    # 编写循环，遍历my_bullet生成子弹图片，然后让子弹可以弹出
    for i in my_bullet:
        screen.blit(bullet, (i['x'], i['y']))
        i['y'] -= 50

# 定义一个主函数main
def main():
    # 创建一个Windows窗口
    screen = pygame.display.set_mode((400, 800), 0, 32)
    # 创建一个background变量，用于存放飞机大战背景图片信息
    background = pygame.image.load('feiji/background.png')
    # 创建一个hero_plane变量，用于存放英雄飞机背景图片信息
    hero = pygame.image.load('feiji/hero1.png')
    # 加载子弹图片
    bullet = pygame.image.load('feiji/plane.png')
    # 加载敌机图片
    enemy = pygame.image.load('feiji/enemy2.png')

    while True:
        # 在Windows窗口中，有一个专门的方法blit()，用于对图片进行粘贴操作（粘贴到窗口中）
        # 窗口对象.blit(要粘贴的图片对象, (横坐标, 纵坐标))
        screen.blit(background, (0, 0))
        # 创建一个函数hero_plane，用于粘贴英雄飞机以及移动飞机等操作
        hero_plane(screen, hero, bullet)
        # 创建一个函数enemy_plane，用于粘贴敌方飞机以及敌方飞机移动操作
        enemy_plane(screen, enemy)

        # 为pygame窗口添加一个标题
        pygame.display.set_caption('飞机大战')
        # 刷新Windows窗口，让图片立即生效
        pygame.display.update()
        # 苹果电脑小伙伴，必须添加以下代码，才能捕获相关的键盘事件
        pygame.event.get()
        # 休眠10s
        time.sleep(0.1)

# 定义程序的入口
if __name__ == '__main__':
    main()