from .. components import info
import pygame


class LoadScreen:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
    def start(self,game_info):
        # 确保使用正确的音乐名称，且音效管理器已初始化
        if self.sound_manager:
            self.sound_manager.play_music('load_screen_theme')  # 使用明确的音乐标识
        self.sound_manager.play_music('invincible')  # 加载界面背景音乐
        self.game_info=game_info
        self.finished=False
        self.next='level'
        self.duration=2000
        self.timer=0
        self.info=info.Info('load_screen',self.game_info)

    def update(self,surface,keys):
        self.draw(surface)
        if self.timer==0:
            self.timer=pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished=True
            self.timer=0

    def draw(self,surface):
        surface.fill((0,0,0))
        self.info.draw(surface)


class GameOver(LoadScreen):
    def start(self,game_info):
        if self.sound_manager:
            self.sound_manager.play_music('game_over_theme')  # 统一命名规范
        self.sound_manager.play_music('game_over')  # 游戏结束音乐
        self.game_info=game_info
        self.finished=False
        self.next='main_menu'
        self.duration=4000
        self.timer=0
        self.info=info.Info('game_over',self.game_info)