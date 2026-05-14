from ..components import info
import pygame
from .. import tools,setup
from .. import constants as C
from .. components import player,stuff,brick,box,enemy
import  os
import json


class Level:
    def __init__(self, sound_manager):  # 新增构造参数
        self.sound_manager = sound_manager
        self.player = None  # 明确声明player属性
        self.castle_reached = False  # 新增状态标记
        self.animation_timer = 0  # 动画计时器


    def setup_player(self):
        self.player = player.Player('mario', self.sound_manager)  # 传递音效管理器
    def start(self,game_info):
        self.game_info = game_info
        self.game_info.update({  # 只更新必要字段
            'time': C.LEVEL_TIME,
            'player_state': 'small'
        })
        self.finished = False
        self.next = 'game_over'
        self.info=info.Info('level',self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_start_positions()
        self.setup_player()
        self.setup_ground_items()
        self.setup_bricks_and_boxes()
        self.setup_enemies()
        self.setup_checkpoints()

    def load_map_data(self):
        file_name='level_1.json'
        file_path=os.path.join('source/data0/maps',file_name)
        with open(file_path) as f:
            self.map_data=json.load(f)

    def setup_background(self):
        self.image_name=self.map_data['image_name']
        self.background=setup.GRAPHICS[self.image_name]
        rect=self.background.get_rect()
        self.background=pygame.transform.scale(self.background,(int(rect.width*C.BG_MULTI),
                                                                     int(rect.height*C.BG_MULTI)))
        self.background_rect=self.background.get_rect()
        self.game_window=setup.SCREEN.get_rect()
        self.game_ground=pygame.Surface((self.background_rect.width,self.background_rect.height))

    def setup_start_positions(self):
        self.positions=[]
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'],data['end_x'],data['player_x'],data['player_y']))
        self.start_x,self.end_x,self.player_x,self.player_y=self.positions[0]

    def setup_player(self):
        """修正：必须先初始化玩家实例再操作属性"""
        # 步骤1：创建玩家实例
        self.player = player.Player('mario', self.sound_manager)

        # 步骤2：设置玩家位置
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

        return self.player  # 返回实例以便链式调用

    def setup_ground_items(self):
        self.ground_items_group=pygame.sprite.Group()
        for name in ['ground','pipe','step']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'],item['y'],item['width'],item['height'],name))

    def setup_bricks_and_boxes(self):
        self.brick_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        # 加载砖块
        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                # 从数据中提取必要参数，使用get避免KeyError
                x = brick_data['x']
                y = brick_data['y']
                brick_type = brick_data.get('type', 0)  # 默认为0（普通砖块）
                color = brick_data.get('color')  # 允许颜色参数为空

                # 根据类型决定奖励分组
                group = None
                if brick_type == 1:  # 包含金币
                    group = self.coin_group
                elif brick_type > 1:  # 包含道具
                    group = self.powerup_group

                # 创建砖块实例并传入必要参数
                self.brick_group.add(
                    brick.Brick(
                        x, y,
                        brick_type=brick_type,
                        group=group,
                        color=color,
                        name='brick',  # 明确指定对象类型
                        game_info=self.game_info,  # 传递计分信息
                        sound_manager = self.sound_manager
                )
                )

        # 加载箱子（单独循环避免参数干扰）
        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x = box_data['x']
                y = box_data['y']
                box_type = box_data.get('type', 0)  # 默认为0

                # 根据类型决定分组
                target_group = self.coin_group if box_type == 1 else self.powerup_group

                # 创建箱子实例
                self.box_group.add(
                    box.Box(
                        x, y,
                        box_type=box_type,
                        group=target_group,
                        name='box',  # 明确指定对象类型
                        game_info=self.game_info,
                        sound_manager=self.sound_manager# 传递计分信息
                    )
                )
    def setup_enemies(self):
        self.dying_group=pygame.sprite.Group()
        self.shell_group=pygame.sprite.Group()
        self.enemy_group=pygame.sprite.Group()
        self.enemy_group_dict={}
        for enemy_group_data in self.map_data['enemy']:
            group=pygame.sprite.Group()
            for enemy_group_id,enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    group.add(enemy.create_enemy(enemy_data, self.sound_manager))
                self.enemy_group_dict[enemy_group_id]=group

    def setup_checkpoints(self):
        self.checkpoint_group=pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x,y,w,h=item['x'],item['y'],item['width'],item['height']
            checkpoint_type=item['type']
            enemy_groupid=item.get('enemy_groupid')
            self.checkpoint_group.add(stuff.Checkpoint(x,y,w,h,checkpoint_type,enemy_groupid))

    def update(self, surface, keys):

        self.current_time=pygame.time.get_ticks()
        self.player.update(keys)

        if self.player.dead:
            if self.current_time - self.player.death_timer>3000:
                 self.finished=True
                 self.update_game_info()

        elif self.is_frozen():
            pass
            # 时间耗尽处理
        elif self.game_info['time'] <= 0 and not self.player.dead:
            self.player.go_die()

        # 更新金币显示
        else:
            self.update_player_position()
            self.check_checkpoints()
            self.check_if_go_die()
            self.update_game_window()
            self.info.update()
            self.brick_group.update()
            self.box_group.update()
            self.enemy_group.update(self)  # ✅ 传递当前level实例给敌人组
            self.dying_group.update(self)
            self.shell_group.update(self)
            self.coin_group.update(self)
            self.powerup_group.update(self)
        self.info.info_labels[4] = (self.create_label('x{:02d}'.format(self.game_info['coin'])), (300, 55))
        self.draw(surface)

    def is_frozen(self):
        return self.player.state in ['small2big','big2small','big2fire','fire2small']

    def update_player_position(self):

        #x direction
        self.player.rect.x+=self.player.x_vel
        if self.player.rect.x<self.start_x:
            self.player.rect.x=self.start_x
        elif self.player.rect.right>self.end_x:
            self.player.rect.right=self.end_x
        self.check_x_collisions()

        #y direction
        if not self.player.dead:
            self.player.rect.y+=self.player.y_vel
            self.check_y_collisions()

    def check_x_collisions(self):
        self.player = self.player
        check_group=pygame.sprite.Group(self.ground_items_group,self.brick_group,self.box_group)
        collided_sprite=pygame.sprite.spritecollideany(self.player,check_group)

        if collided_sprite:
            self.adjust_player_x(collided_sprite)

        if self.player.hurt_immune:
            return

        enemy=pygame.sprite.spritecollideany(self.player,self.enemy_group)

        if enemy:
            # 只在第一次碰撞时计分
            if not enemy.had_scored:  # 添加标记字段
                self.game_info['score'] += 100 if enemy.name == 'goomba' else 200
                enemy.had_scored = True

            if self.player.big:
                self.player.state = 'big2small'
                self.player.hurt_immune = True
            else:
                self.player.go_die()

        shell=pygame.sprite.spritecollideany(self.player,self.shell_group)
        if shell:
            if shell.state=='slide':
                self.player.go_die()
            else:
                if self.player.rect.x<shell.rect.x:
                    shell.x_vel=10
                    shell.rect.x+=40
                    shell.diretion=1
                else:
                    shell.x_vel = -10
                    shell.rect.x -= 40
                    shell.diretion = 0
                shell.state='slide'

        powerup=pygame.sprite.spritecollideany(self.player,self.powerup_group)
        if powerup:
            powerup.kill()
            if powerup.name=='mushroom':
                self.player.state='small2big'
        if powerup:
            self.sound_manager.on_powerup()  # 触发道具音效
            powerup.kill()

    def check_y_collisions(self):

        ground_item=pygame.sprite.spritecollideany(self.player,self.ground_items_group)
        brick=pygame.sprite.spritecollideany(self.player,self.brick_group)
        box=pygame.sprite.spritecollideany(self.player,self.box_group)
        enemy=pygame.sprite.spritecollideany(self.player,self.enemy_group)

        if brick and box:
            to_brick=abs(self.player.rect.centerx-brick.rect.centerx)
            to_box=abs(self.player.rect.centerx-box.rect.centerx)
            if to_brick>to_box:
                brick=None
            else:
                box=None

        if ground_item:
            self.adjust_player_y(ground_item)
        elif brick:
            self.adjust_player_y(brick)
        elif box:
            self.adjust_player_y(box)
        elif enemy:
            self.game_info['score'] += 100 if enemy.name == 'goomba' else 200
            if not enemy.had_scored:
                self.game_info['score'] += 100 if enemy.name == 'goomba' else 200
                enemy.had_scored = True
            if self.player.hurt_immune:
                return
            self.enemy_group.remove(enemy)
            if enemy.name=='koopa':
                self.shell_group.add(enemy)
            else:
                self.dying_group.add(enemy)

            if self.player.y_vel<0:
                how='bumped'
            else:
                how='trampled'
                self.player.state='jump'
                self.player.rect.bottom=enemy.rect.top
                self.player.y_vel=self.player.jump_vel*0.8
            enemy.go_die(how)

        self.check_will_fall(self.player)
        if enemy:
            self.sound_manager.on_enemy_stomp()  # 触发踩敌人音效

    def adjust_player_x(self,sprite):
        if self.player.rect.x<sprite.rect.x:
            self.player.rect.right=sprite.rect.left

        else:
            self.player.rect.left=sprite.rect.right
        self.player.x_vel=0

    def adjust_player_y(self, sprite):
        #downwards
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.y_vel = 0
            self.player.rect.bottom=sprite.rect.top
            self.player.state='walk'
        #upwards
        else:
            self.player.y_vel = 7
            self.player.rect.top = sprite.rect.bottom
            self.player.state='fall'

            if sprite.name=='box':
                if sprite.state=='rest':
                    sprite.go_bumped()
            if sprite.name == 'brick':
                if sprite.state == 'rest':
                    sprite.go_bumped()
                    # 修改点：立即更新分数显示
                    self.info.update()

    def check_will_fall(self,sprite):
        sprite.rect.y+=1
        check_group=pygame.sprite.Group(self.ground_items_group,self.brick_group,self.box_group)
        collided_sprite=pygame.sprite.spritecollideany(sprite,check_group)
        if not collided_sprite and sprite.state!='jump' and not self.is_frozen():
            sprite.state='fall'
        sprite.rect.y-=1

    def update_game_window(self):
        third=self.game_window.x+self.game_window.width/3
        if self.player.x_vel>0 and self.player.rect.centerx>third and self.game_window.right<self.end_x:
            self.game_window.x+=self.player.x_vel
            self.start_x=self.game_window.x

    def draw(self, surface):
        self.game_ground.blit(self.background,self.game_window,self.game_window)
        self.game_ground.blit(self.player.image,self.player.rect)
        self.powerup_group.draw(self.game_ground)
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        self.enemy_group.draw(self.game_ground)
        self.dying_group.draw(self.game_ground)
        self.shell_group.draw(self.game_ground)
        self.coin_group.draw(self.game_ground)

        surface.blit(self.game_ground,(0,0),self.game_window)
        self.info.draw(surface)

    def check_checkpoints(self):
        checkpoint=pygame.sprite.spritecollideany(self.player,self.checkpoint_group)
        if checkpoint:
            if checkpoint.checkpoint_type==0:#checkpoint for enemy appearance
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_groupid)])
            checkpoint.kill()

    def check_if_go_die(self):
        if self.player.rect.y>C.SCREEN_H:
            self.player.go_die()

    def update_game_info(self):
        if self.player.dead:
            self.sound_manager.on_player_death()  # 触发死亡音效
        # 修改点：添加生命值下限保护
        if self.player.dead:
            self.game_info['lives'] = max(0, self.game_info['lives'] - 1)  # 确保生命值不低于0

        # 修改点：根据剩余生命值决定下一状态
        if self.game_info['lives'] <= 0:
            self.next = 'game_over'
            # 重置生命值为初始值，避免下次游戏出现负数
            self.game_info['lives'] = 3
        else:
            self.next = 'load_screen'
            # 确保返回加载画面时携带正确的生命值
            self.game_info['lives'] = self.game_info['lives']

    def create_label(self, text, size=40):
        font = pygame.font.SysFont(C.FONT, size)
        label = font.render(text, True, (255, 255, 255))
        return label