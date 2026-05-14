# sound.py
import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7

        # 定义音效路径结构
        self.paths = {
            'music': {
                'main_theme': 'resources/music/main_theme.ogg',
                'invincible': 'resources/music/invincible.ogg',
                'game_over': 'resources/music/game_over.ogg'
            },
            'sfx': {
                # 系统音效
                'death': 'resources/music/death.wav',
                'coin': 'resources/sound/coin.ogg',
                # 动作音效
                'jump': 'resources/sound/small_jump.ogg',
                'big_jump': 'resources/sound/big_jump.ogg',
                'stomp': 'resources/sound/stomp.ogg',
                # 道具音效
                'powerup': 'resources/sound/powerup.ogg',
                'fireball': 'resources/sound/fireball.ogg',
                # 场景音效
                'pipe': 'resources/sound/pipe.ogg',
                'brick_smash': 'resources/sound/brick_smash.ogg'
            }
        }

        # 加载所有音效
        self.load_all()

    def load_all(self):
        """加载所有定义好的音效"""
        try:
            # 加载音乐类音频
            for name, path in self.paths['music'].items():
                pygame.mixer.music.load(path)

            # 加载音效类音频
            for name, path in self.paths['sfx'].items():
                self.sounds[name] = pygame.mixer.Sound(path)
                self.sounds[name].set_volume(self.sfx_volume)

        except pygame.error as e:
            print(f"音效加载失败: {str(e)}")
        except FileNotFoundError as e:
            print(f"音效文件缺失: {str(e)}")

    # ---------- 音乐控制 ----------
    def play_music(self, name, loops=-1):
        """播放背景音乐"""
        if name in self.paths['music']:
            pygame.mixer.music.load(self.paths['music'][name])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    # ---------- 音效触发 ----------
    def play_sfx(self, name):
        """播放音效（单次）"""
        if name in self.sounds:
            self.sounds[name].play()

    # ---------- 游戏事件绑定 ----------
    def on_player_death(self):
        self.play_sfx('death')
        self.stop_music()

    def on_coin_collect(self):
        self.play_sfx('coin')

    def on_jump(self, is_big=False):
        self.play_sfx('big_jump' if is_big else 'jump')

    def on_powerup(self):
        self.play_sfx('powerup')

    def on_enemy_stomp(self):
        self.play_sfx('stomp')

    def on_pipe_enter(self):
        self.play_sfx('pipe')

    def on_brick_break(self):
        self.play_sfx('brick_smash')
