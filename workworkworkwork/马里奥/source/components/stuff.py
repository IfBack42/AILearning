import  pygame


class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h,name):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((w,h)).convert()
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.name=name

class Checkpoint(Item):
    def __init__(self, x, y, w, h, checkpoint_type, enemy_groupid=None, name='checkpoint'):
        super().__init__(x, y, w, h, name)
        self.checkpoint_type = checkpoint_type  # 0-敌人 1-城堡
        self.enemy_groupid = enemy_groupid