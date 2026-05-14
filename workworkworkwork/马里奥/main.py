# 游戏主要入口
from source import tools
from source.states import main_menu, load_screen, level
from source.sound import SoundManager  # 修正导入路径


def main():
    # 初始化声音管理器
    sound_manager = SoundManager()
    sound_manager.play_music('main_theme')  # 播放主背景音乐

    state_dict = {
        'main_menu': main_menu.MainMenu(sound_manager),
        'load_screen': load_screen.LoadScreen(sound_manager),
        'level': level.Level(sound_manager),
        'game_over': load_screen.GameOver(sound_manager),
              }
    game = tools.Game(state_dict, 'main_menu')
    game.run()


if __name__ == '__main__':
    main()