import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    #初始化飞船并设置其初始位置
    def __init__(self,ai_settings,screen):
        super(Ship, self).__init__()
        self.screen = screen
        #加载其外形
        self.image = pygame.image.load('image/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        #将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.center = float(self.rect.centerx)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:#self.moving_right是一个判断命令
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor
        #根据self.center更新rect对象
        self.rect.centerx = self.center


    def blitme(self):
        """在指定的位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
