import pygame
from .. import tools,setup
from .. import  constants as C
from .powerup import create_powerup


class Box(pygame.sprite.Sprite):
    def __init__(self,x,y,box_type,group,name='box',game_info=None, sound_manager=None):
        self.game_info = game_info  # 从外部传入
        self.sound_manager = sound_manager  # 新增音效管理器
        pygame.sprite.Sprite.__init__(self)
        self.game_info = game_info  # 从外部传入
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.box_type=box_type
        self.group=group
        self.name=name
        self.frame_rects=[
            (384,0,16,16),
            (400,0,16,16),
            (416,0,16,16),
            (432,0,16,16),
        ]

        self.frames=[]
        for frame_rect in self.frame_rects:
            self.frames.append(tools.get_image(setup.GRAPHICS['tile_set'],*frame_rect,(0,0,0),C.BRICK_MULTI))

        self.frame_index=0
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        self.gravity=C.GRAVITY

        self.state='rest'
        self.timer=0

    def update(self):
        self.current_time=pygame.time.get_ticks()
        self.handle_states()

    def handle_states(self):
        if self.state=='rest':
            self.rest()
        elif self.state=='bumped':
            self.bumped()
        elif self.state=='open':
            self.open()

    def rest(self):
        frame_durations=[400,100,100,50]
        if self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index=(self.frame_index+1)%4
            self.timer=self.current_time
        self.image=self.frames[self.frame_index]

    def go_bumped(self):
        self.y_vel = -7
        self.state = 'bumped'
        if self.game_info:
            self.game_info['score'] += 200 if self.box_type != 1 else 50
        if self.sound_manager:
            self.sound_manager.on_brick_break()  # 使用砖块破裂通用音效

    def bumped(self):
        self.rect.y+=self.y_vel
        self.y_vel+=self.gravity
        self.frame_index=3
        self.image=self.frames[self.frame_index]

        if self.rect.y>self.y+5:
            self.rect.y=self.y
            self.state='open'

            #box=0,1,2,3对应 空，金币，星星，蘑菇
            if self.box_type==1:
                pass
            else:
                self.group.add(create_powerup(self.rect.centerx,self.rect.centery,self.box_type))

                # 移动计分逻辑到此处，确保只触发一次
            if self.game_info:
                self.game_info['score'] += 200 if self.box_type != 1 else 50  # 调整判断逻辑

    def open(self):
        pass